from common_files import auth_helper as AH
from common_files import reporting_example_helper 
from common_files import customermanagement_example_helper as CH
from bingads.v13.reporting import *
from datetime import date, timedelta, datetime

from common_files import PushToS3 as PTS
from common_files import GetHighWaterMark as GHWM

# The report file extension type.
REPORT_FILE_FORMAT='Csv'
CURRENT_TIME = datetime.now().strftime("%Y%m%d%H%M%S")

FILE_DIRECTORY='/tmp/'

# The name of the report download file.
PREFIX = 'CampaignsCostAttributionHistory/'
RESULT_FILE_NAME='CampaignsCostAttributionHistory.' + CURRENT_TIME + '.' + REPORT_FILE_FORMAT.lower()

# The maximum amount of time (in milliseconds) that you want to wait for the report download.
TIMEOUT_IN_MILLISECONDS=3600000



def background_completion(reporting_download_parameters):
    """ You can submit a download request and the ReportingServiceManager will automatically 
    return results. The ReportingServiceManager abstracts the details of checking for result file 
    completion, and you don't have to write any code for results polling. """

    global reporting_service_manager
    result_file_path = reporting_service_manager.download_file(reporting_download_parameters)
    CH.output_status_message("Download result file: {0}".format(result_file_path))

def submit_and_download(report_request,reporting_service_manager):
    """ Submit the download request and then use the ReportingDownloadOperation result to 
    track status until the report is complete e.g. either using
    ReportingDownloadOperation.track() or ReportingDownloadOperation.get_status(). """

    #global reporting_service_manager
    reporting_download_operation = reporting_service_manager.submit_download(report_request)

    # You may optionally cancel the track() operation after a specified time interval.
    reporting_operation_status = reporting_download_operation.track(timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS)

    
    result_file_path = reporting_download_operation.download_result_file(
        result_file_directory = FILE_DIRECTORY, 
        result_file_name = RESULT_FILE_NAME, 
        decompress = True, 
        overwrite = True,  # Set this value true if you want to overwrite the same file.
        timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS # You may optionally cancel the download after a specified time interval.
    )
    
    CH.output_status_message("Download result file: {0}".format(result_file_path))

def download_results(request_id, authorization_data):
    """ If for any reason you have to resume from a previous application state, 
    you can use an existing download request identifier and use it 
    to download the result file. Use ReportingDownloadOperation.track() to indicate that the application 
    should wait to ensure that the download status is completed. """
    
    reporting_download_operation = ReportingDownloadOperation(
        request_id = request_id, 
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=1000, 
        environment=ENVIRONMENT,
    )

    reporting_operation_status = reporting_download_operation.track(timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS)
    
    result_file_path = reporting_download_operation.download_result_file(
        result_file_directory = FILE_DIRECTORY, 
        result_file_name = RESULT_FILE_NAME, 
        decompress = True, 
        overwrite = True,  # Set this value true if you want to overwrite the same file.
        timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS # You may optionally cancel the download after a specified time interval.
    ) 

    CH.output_status_message("Download result file: {0}".format(result_file_path))
    CH.output_status_message("Status: {0}".format(reporting_operation_status.status))

def download_report(reporting_download_parameters):
    """ You can get a Report object by submitting a new download request via ReportingServiceManager. 
    Although in this case you will not work directly with the file, under the covers a request is 
    submitted to the Reporting service and the report file is downloaded to a local directory.  """
    
    global reporting_service_manager

    report_container = reporting_service_manager.download_report(reporting_download_parameters)


    if(report_container == None):
        CH.output_status_message("There is no report data for the submitted report request parameters.")
        sys.exit(0)


    record_count = report_container.record_count
    CH.output_status_message("ReportName: {0}".format(report_container.report_name))
    CH.output_status_message("ReportTimeStart: {0}".format(report_container.report_time_start))
    CH.output_status_message("ReportTimeEnd: {0}".format(report_container.report_time_end))
    CH.output_status_message("LastCompletedAvailableDate: {0}".format(report_container.last_completed_available_date))
    CH.output_status_message("ReportAggregation: {0}".format(report_container.report_aggregation))
    CH.output_status_message("ReportColumns: {0}".format("; ".join(str(column) for column in report_container.report_columns)))
    CH.output_status_message("ReportRecordCount: {0}".format(record_count))

    #Analyze and output performance statistics

    if "Impressions" in report_container.report_columns and \
        "Clicks" in report_container.report_columns and \
        "DeviceType" in report_container.report_columns and \
        "Network" in report_container.report_columns:

        report_record_iterable = report_container.report_records

        total_impressions = 0
        total_clicks = 0
        distinct_devices = set()
        distinct_networks = set()
        for record in report_record_iterable:
            total_impressions += record.int_value("Impressions")
            total_clicks += record.int_value("Clicks")
            distinct_devices.add(record.value("DeviceType"))
            distinct_networks.add(record.value("Network"))

        CH.output_status_message("Total Impressions: {0}".format(total_impressions))
        CH.output_status_message("Total Clicks: {0}".format(total_clicks))
        CH.output_status_message("Average Impressions: {0}".format(total_impressions * 1.0 / record_count))
        CH.output_status_message("Average Clicks: {0}".format(total_clicks * 1.0 / record_count))
        CH.utput_status_message("Distinct Devices: {0}".format("; ".join(str(device) for device in distinct_devices)))
        CH.output_status_message("Distinct Networks: {0}".format("; ".join(str(network) for network in distinct_networks)))

    #Be sure to close the report.

    report_container.close()

def get_report_request(account_id,reporting_service,DateRangeLastDate):
    """ 
    Use a sample report request or build your own. 
    """
    

    aggregation = 'Daily'
    exclude_column_headers=False
    exclude_report_footer=True
    exclude_report_header=True
    time=reporting_service.factory.create('ReportTime')
    # You can either use a custom date range or predefined time.
    time.CustomDateRangeEnd.Day=30
    time.CustomDateRangeEnd.Month=8
    time.CustomDateRangeEnd.Year=2020
    time.CustomDateRangeStart.Day=10
    time.CustomDateRangeStart.Month=3
    time.CustomDateRangeStart.Year=2018
    time.ReportTimeZone='CanberraMelbourneSydney'
    return_only_complete_data=False

    #BudgetSummaryReportRequest does not contain a definition for Aggregation.
    budget_summary_report_request=get_budget_summary_report_request(
        account_id=account_id,
        exclude_column_headers=exclude_column_headers,
        exclude_report_footer=exclude_report_footer,
        exclude_report_header=exclude_report_header,
        report_file_format=REPORT_FILE_FORMAT,
        return_only_complete_data=return_only_complete_data,
        time=time,
        reporting_service=reporting_service)

    campaign_performance_report_request=get_campaign_performance_report_request(
        account_id=account_id,
        aggregation=aggregation,
        exclude_column_headers=exclude_column_headers,
        exclude_report_footer=exclude_report_footer,
        exclude_report_header=exclude_report_header,
        report_file_format=REPORT_FILE_FORMAT,
        return_only_complete_data=return_only_complete_data,
        time=time,
        reporting_service=reporting_service)

    keyword_performance_report_request=get_keyword_performance_report_request(
        account_id=account_id,
        aggregation=aggregation,
        exclude_column_headers=exclude_column_headers,
        exclude_report_footer=exclude_report_footer,
        exclude_report_header=exclude_report_header,
        report_file_format=REPORT_FILE_FORMAT,
        return_only_complete_data=return_only_complete_data,
        time=time,
        reporting_service=reporting_service)

    user_location_performance_report_request=get_user_location_performance_report_request(
        account_id=account_id,
        aggregation=aggregation,
        exclude_column_headers=exclude_column_headers,
        exclude_report_footer=exclude_report_footer,
        exclude_report_header=exclude_report_header,
        report_file_format=REPORT_FILE_FORMAT,
        return_only_complete_data=return_only_complete_data,
        time=time,
        reporting_service=reporting_service)

    return campaign_performance_report_request

def get_budget_summary_report_request(
        account_id,
        exclude_column_headers,
        exclude_report_footer,
        exclude_report_header,
        report_file_format,
        return_only_complete_data,
        time,
        reporting_service):

    report_request=reporting_service.factory.create('BudgetSummaryReportRequest')
    report_request.ExcludeColumnHeaders=exclude_column_headers
    report_request.ExcludeReportFooter=exclude_report_footer
    report_request.ExcludeReportHeader=exclude_report_header
    report_request.Format=report_file_format
    report_request.ReturnOnlyCompleteData=return_only_complete_data
    report_request.Time=time    
    report_request.ReportName="My Budget Summary Report"
    scope=reporting_service.factory.create('AccountThroughCampaignReportScope')
    scope.AccountIds={'long': [account_id] }
    scope.Campaigns=None
    report_request.Scope=scope     

    report_columns=reporting_service.factory.create('ArrayOfBudgetSummaryReportColumn')
    report_columns.BudgetSummaryReportColumn.append([
        'AccountName',
        'AccountNumber',
        'AccountId',
        'CampaignName',
        'CampaignId',
        'Date',
        'CurrencyCode',
        'MonthlyBudget',
        'DailySpend',
        'MonthToDateSpend'
    ])
    report_request.Columns=report_columns

    return report_request

def get_campaign_performance_report_request(
        account_id,
        aggregation,
        exclude_column_headers,
        exclude_report_footer,
        exclude_report_header,
        report_file_format,
        return_only_complete_data,
        time,
        reporting_service):

    report_request=reporting_service.factory.create('CampaignPerformanceReportRequest')
    report_request.Aggregation=aggregation
    report_request.ExcludeColumnHeaders=exclude_column_headers
    report_request.ExcludeReportFooter=exclude_report_footer
    report_request.ExcludeReportHeader=exclude_report_header
    report_request.Format=report_file_format
    report_request.ReturnOnlyCompleteData=return_only_complete_data
    report_request.Time=time    
    report_request.ReportName="My Campaign Performance Report"
    scope=reporting_service.factory.create('AccountThroughCampaignReportScope')
    scope.AccountIds={'long': [account_id] }
    scope.Campaigns=None
    report_request.Scope=scope     

    report_columns=reporting_service.factory.create('ArrayOfCampaignPerformanceReportColumn')
    report_columns.CampaignPerformanceReportColumn.append([
        'TimePeriod',
        'AccountName',
        'CampaignName',
        'CampaignStatus',
        'Impressions',
        'Clicks',  
        'Spend',
        'AveragePosition',
        'Conversions',
        'ConversionRate',
        'AllConversions',
        'AllConversionRate',
        'AverageCpc'
    ])
    report_request.Columns=report_columns
    
    return report_request

def get_keyword_performance_report_request(
        account_id,
        aggregation,
        exclude_column_headers,
        exclude_report_footer,
        exclude_report_header,
        report_file_format,
        return_only_complete_data,
        time,
        reporting_service):

    report_request=reporting_service.factory.create('KeywordPerformanceReportRequest')
    report_request.Aggregation=aggregation
    report_request.ExcludeColumnHeaders=exclude_column_headers
    report_request.ExcludeReportFooter=exclude_report_footer
    report_request.ExcludeReportHeader=exclude_report_header
    report_request.Format=report_file_format
    report_request.ReturnOnlyCompleteData=return_only_complete_data
    report_request.Time=time    
    report_request.ReportName="My Keyword Performance Report"
    scope=reporting_service.factory.create('AccountThroughAdGroupReportScope')
    scope.AccountIds={'long': [account_id] }
    scope.Campaigns=None
    scope.AdGroups=None
    report_request.Scope=scope     

    report_columns=reporting_service.factory.create('ArrayOfKeywordPerformanceReportColumn')
    report_columns.KeywordPerformanceReportColumn.append([
        'TimePeriod',
        'AccountId',
        'CampaignId',
        'Keyword',
        'KeywordId',
        'DeviceType',
        'Network',
        'Impressions',
        'Clicks',  
        'Spend',
        'BidMatchType',              
        'Ctr',
        'AverageCpc',        
        'QualityScore'
    ])
    report_request.Columns=report_columns

    return report_request

def get_user_location_performance_report_request(
        account_id,
        aggregation,
        exclude_column_headers,
        exclude_report_footer,
        exclude_report_header,
        report_file_format,
        return_only_complete_data,
        time,
        reporting_service):
    
    report_request=reporting_service.factory.create('UserLocationPerformanceReportRequest')
    report_request.Aggregation=aggregation
    report_request.ExcludeColumnHeaders=exclude_column_headers
    report_request.ExcludeReportFooter=exclude_report_footer
    report_request.ExcludeReportHeader=exclude_report_header
    report_request.Format=report_file_format
    report_request.ReturnOnlyCompleteData=return_only_complete_data
    report_request.Time=time    
    report_request.ReportName="My User Location Performance Report"
    scope=reporting_service.factory.create('AccountThroughAdGroupReportScope')
    scope.AccountIds={'long': [account_id] }
    scope.Campaigns=None
    scope.AdGroups=None
    report_request.Scope=scope 

    report_columns=reporting_service.factory.create('ArrayOfUserLocationPerformanceReportColumn')
    report_columns.UserLocationPerformanceReportColumn.append([
        'TimePeriod',
        'AccountId',
        'AccountName',
        'CampaignId',
        'AdGroupId',
        'LocationId',
        'Country',
        'Clicks',
        'Impressions',
        'DeviceType',
        'Network',
        'Ctr',
        'AverageCpc',
        'Spend',
    ])
    report_request.Columns=report_columns

    return report_request

# Main execution
def main_report_requets():

    print("Loading the web service client proxies...")

    authorization_data=AH.AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token='116CT48D22861292',
        authentication=None,
    )

    reporting_service_manager=ReportingServiceManager(
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=5000, 
        environment='production',
    )

    # In addition to ReportingServiceManager, you will need a reporting ServiceClient 
    # to build the ReportRequest.

    reporting_service=ServiceClient(
        service='ReportingService', 
        version=13,
        authorization_data=authorization_data, 
        environment='production',
    )

    customer_service=ServiceClient(
        service='CustomerManagementService', 
        version=13,
        authorization_data=authorization_data, 
        environment='production',
    )
        


    AH.authenticate(authorization_data)
        
    try:

        DateRangeLastDate = GHWM.get_highwatermark(os.environ['targetbucket'],PREFIX,'2018-03-09')
        if (DateRangeLastDate >= (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")):
            return 

        account_id=[]
        get_account_response=customer_service.GetAccountsInfo()
        if get_account_response is None or len(get_account_response) == 0:
            return
        for get_account_id in get_account_response['AccountInfo']:
            account_id.append(get_account_id.Id)


        report_request=get_report_request(account_id,reporting_service,DateRangeLastDate) 
        reporting_download_parameters = ReportingDownloadParameters(
            report_request=report_request,            
            result_file_directory = FILE_DIRECTORY, 
            result_file_name = RESULT_FILE_NAME, 
            overwrite_result_file = True, # Set this value true if you want to overwrite the same file.
            timeout_in_milliseconds=TIMEOUT_IN_MILLISECONDS # You may optionally cancel the download after a specified time interval.
        )


        CH.output_status_message("-----\nAwaiting Submit and Download...")
        submit_and_download(report_request,reporting_service_manager)

        
        PTS.push_to_s3(FILE_DIRECTORY,PREFIX,RESULT_FILE_NAME,(date.today() - timedelta(days=1)).strftime("%Y-%m-%d"))
        

    except AH.WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        CH.output_status_message(ex)