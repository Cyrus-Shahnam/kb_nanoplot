
from installed_clients.ReadsUtilsClient import ReadsUtils
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil


def upload_reads(callback_url, read_path, workspace_name, obj_name):
    ru = ReadsUtils(callback_url)
    return ru.upload_reads({
        'fwd_file': read_path,
        'sequencing_tech': 'Nanopore',
        'name': obj_name,
        'workspace_name': workspace_name
    })


def run_Nanoplot(callback_url, input_reads_ref, output_workspace, output_name):
    """
    Run NanoPlot on the specified FASTQ reads.

    Parameters
    ----------
    callback_url : str
        The callback URL from the KBase environment.
    input_reads_ref : str
        KBase reference to the input reads object.
    output_workspace : str
        Name of the workspace where the output will be saved.
    output_name : str
        Base name for output files and report.
    """

    # Set up clients
    dfu = DataFileUtil(callback_url)
    ru = ReadsUtils(callback_url)
    report_client = KBaseReport(callback_url)

    # Create working directory
    work_dir = os.path.join('/kb/module/work/tmp', str(uuid.uuid4()))
    os.makedirs(work_dir, exist_ok=True)

    # Download reads
    reads_info = ru.download_reads({
        'read_libraries': [input_reads_ref],
        'interleaved': False,
        'deinterleaved': False
    })
    fastq_path = reads_info['files'][input_reads_ref]['files']['fwd']

    # Run NanoPlot
    output_dir = os.path.join(work_dir, 'nanoplot_output')
    os.makedirs(output_dir, exist_ok=True)

    nanoplot_cmd = [
        'NanoPlot',
        '--fastq', fastq_path,
        '--outdir', output_dir,
        '--plots', 'dot'
    ]

    subprocess.run(nanoplot_cmd, check=True)

    # Compress NanoPlot output for report
    output_zip = os.path.join(work_dir, f"{output_name}_NanoPlot.zip")
    shutil.make_archive(output_zip.replace(".zip", ""), 'zip', output_dir)

    shock_id = dfu.file_to_shock({'file_path': output_zip, 'make_handle': 0, 'pack': 'zip'})['shock_id']

    report_output = report_client.create_extended_report({
        'direct_html_link_index': 0,
        'html_links': [{
            'shock_id': shock_id,
            'name': f"{output_name}_NanoPlot.zip",
            'label': "NanoPlot output"
        }],
        'report_object_name': f"{output_name}_NanoPlot_report",
        'workspace_name': output_workspace
    })

    return report_output
