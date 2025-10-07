#BEGIN_HEADER
import os
import logging
import sys
import traceback
import subprocess
import uuid

from installed_clients.ReadsUtilsClient import ReadsUtils
from installed_clients.KBaseReportClient import KBaseReport
from .Utils.createHtmlReport import HTMLReportCreator
from .Utils.run_NanoplotUtils import run_Nanoplot, upload_reads

#END_HEADER

#BEGIN_CLASS_HEADER

class kb_nanoplot:
    '''
    Module Name:
    kb_nanoplot

    Module Description:
    A KBase module that runs NanoPlot on SingleEndLibrary FASTQ reads and generates a report.
    '''

    VERSION = "0.0.1"
    GIT_URL = "https://github.com/Cyrus-Shahnam/kb_nanoplot.git"
    GIT_COMMIT_HASH = "REPLACE_WITH_ACTUAL_COMMIT_HASH"

#END_CLASS_HEADER

    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.scratch = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR

    #BEGIN run_kb_nanoplot
    def run_kb_nanoplot(self, ctx, params):
        logging.info("Starting NanoPlot run")
        
        # Download reads
        reads_ref = params['reads_input_ref']
        logging.info(f"Fetching reads: {reads_ref}")
        
        self.ru = ReadsUtils(self.callback_url)
        reads_info = self.ru.download_reads({
            'read_libraries': [reads_ref],
            'interleaved': "false",
            'gzipped': True
        })

        fastq_path = reads_info['files'][reads_ref]['files']['fwd']
        logging.info(f"Downloaded FASTQ file to: {fastq_path}")

        # Set up output directory
        output_dir = os.path.join(self.scratch, "nanoplot_output")
        os.makedirs(output_dir, exist_ok=True)

        # Run NanoPlot
        cmd = [
            'NanoPlot',
            '--fastq', fastq_path,
            '--outdir', output_dir,
            "--loglength",
            '--N50'
        ]

        logging.info(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

        # Find HTML report
        html_report_path = os.path.join(output_dir, "NanoPlot-report.html")
        if not os.path.exists(html_report_path):
            raise FileNotFoundError("NanoPlot report not found.")

        # Copy to scratch root for upload
        copied_html_path = os.path.join(self.scratch, "NanoPlot-report.html")
        os.rename(html_report_path, copied_html_path)

        # Generate report
        report_client = KBaseReport(self.callback_url)
        report_info = report_client.create_extended_report({
            'direct_html_link_index': 0,
            'html_links': [{
                'name': 'NanoPlot-report.html',
                'path': copied_html_path
            }],
            'report_object_name': 'nanoplot_report_' + str(uuid.uuid4()),
            'workspace_name': params['workspace_name']
        })

        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref']
        }

        return [output]
    #END run_kb_nanoplot

#BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
#END_STATUS
def run_userNameModulename(self, ctx, params):
        # Create a report
        report_creator = HTMLReportCreator(self.callback_url)
        output = report_creator.create_html_report(reportDirectory, params['workspace_name'], objects_created)
        logging.info ('HTML output report: ' + str(output))
        corrected_file_name = returned_dict['corrected_file_name']
        corrected_file_path = returned_dict['corrected_file_path']
        logging.info('Corrected file path: ' + corrected_file_path)
        logging.info('Corrected file name: ' + corrected_file_name)


