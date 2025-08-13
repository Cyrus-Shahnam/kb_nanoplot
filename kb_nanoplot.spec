/*
A KBase module: kb_nanoplot
*/

module kb_nanoplot {
    /*
        Output structure with a reference to a KBaseReport
    */
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This method runs NanoPlot on a KBaseFile.SingleEndLibrary
        and returns a KBaseReport with a link to the NanoPlot HTML output.
    */
    funcdef run_kb_nanoplot(mapping<string, UnspecifiedObject> params) returns (ReportResults output) authentication required;
};
