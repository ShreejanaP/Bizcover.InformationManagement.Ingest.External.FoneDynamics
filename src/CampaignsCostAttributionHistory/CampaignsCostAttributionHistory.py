import json
from src.CampaignsCostAttributionHistory import report_requests as RR

def handler(event, context):
  try:
    RR.main_report_requets()
    response = {
      'status': 200
    }
  except Exception as error:
    response = {
      'status': 500,
      'error': {
        'type': type(error).__name__,
        'description': str(error),
        },
    }
  finally:
    print(response)
    return response

