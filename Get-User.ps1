$accessToken = "eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkExMjhDQkMtSFMyNTYiLCJ4NXQiOiJFVkJyR1ZJZkRubnB5LXkybFE2NWVkVFJRUmsiLCJ6aXAiOiJERUYifQ.ACqZYrkXAHytOgoi_zs8wyczQUEBJOJGIGRZI07NpE_djWPfsAsVFUmBvctIw7EYeYenKZirB4xU5aoihdPKIb9Pr_jSPdkBJlpMGxcx0rOf9jRCjnG6TyD7wrEBhLOb4gdj9uFM_sdhY-uBz2tlc24pN0I5CI_IoGt2lMu3BYwlfWMPXR_r3c4dtDaStGGUYvD763N8DKXiSBOJtL1lAVq6YqXLAaaipjQ2cutt92xkVz0wRGJFp477F7PmKbHpjF8DxkTABqk0eEzD67F9iP0EYOR2-hziPQMqVxQhLrv6fgxsmo3bmIcJ4bXCRqw_uvD4t7VD638b1Pz9cTYPLA.p7k13vbCZr6NFgEZo2b9Ig.pqTVAMT5HQGxGLSV6d0PdUxSpq-C5Uh92AIOIGI6Xb6MqFP5SbBgA3SpfJCp9tmIWTJsR1c5wtHKrJP_5pOp_DJMybkG24arcIQ7P6st-w2SyDoOjFoNK69dXgdWT21-7wxOxsWuBCWEo1F0RMmBqwQSpoK2ebWp7t4GqipoQHJflt-n3gurlO15obVAUKT_K49aR9lujt28q_ZEvfLYFOvCrZ7xW1DhZ8ro5FtPL8bKV9UZFziY2AIqX39Bj14iNLDP9PdwQL03AIuguCZpIMY5GnqCPJK6lS-6iH3YMKR8GiHNg2pHR_4RlrWVfdEIW3NbrQPIWEv6hqKX8raA5Z2QP8C7ktut0aH2LanQxDqSkq78GuqE8GaRGWj4lAVAVaiNU7SYw5g2QYtQN9h3qtnzTeF1RqkcoDS_ZMXnfaF6C4ZLSFLZDuoBExN7X0cU53EnkFbN5b_KdCLTNlzc7-GHwsmGg_2Z87RdDtEEyRVyfZaCXpkImIwPwC8q9zRmHcBi-_wmxSK3zU0JgCboEyN-29afKXSd598WBbjbthdowR86tPF7Hi19HDNy4W4I1U6vOZ1pk5sIOJBTXzIDwJaGxbXVL6wz5kDj0SwF5Fy7jYo2_EEc2aVK33biDbIA19Wu8zBrxH555zpCuKn-NOYMoITOdVC-azOENg0r2LmchcdKQUkeBo_xmTSI_z939WWdlf0A5jAiOds19nTGiD0ljbYuPcEgaFGdtrgCnK7KbTYrZYFDo2rAfA-cuPGMP7fr_hKQTGDlbQYj3Sm5foVwgC_YZwXTXQVNL0ALLF5jPja5BTRtoO2cohDlYs7iMevldGX1zq8PtE8nJyjfuJzEqoM_Vz47gIu0-9Wv5lNaudQ29eAxNWS2s2tQMy3pyANWIjBTsUeAXf5nDHa7tnQrukv-aTPje-AyAHRI-LSiPcOvJpzs1Rd0fYzI-sjYKwwszuXhJhUFisZpSDwW93W3ygWRe3Ip3CNbg37xDSY7oOn1Um6pcP4ULvwcF0W7_okAGU9W737K6ClV42gaQOn08mfsFNkz7OZ-BwN509s3mh20jtk_dbzmzqweoDQy8Df-U547SNlGCfpsxFeF7GyYXyD0Vkn6V5cq0vV_oWvurZsgCphUdVl2tRSSNvJfs2HTIpfM5pkr2JbGXFmHoE0Zq5siTD0yIrcqg1IsbX3guNztiYOLSaAVbq4Y3fkZLrvhNHY8VTnsMsZ1Bep8BcWxwZa_oguzOeuYtD8tQCDYcTr9CB5EY0dPqBXcRf6AK-Hvaf-TPc6aTzDhfUA5dw.pOO5Gmn82KN13ccMNwbv8w";
$developerToken = "116CT48D22861292";

[xml]$getUserRequest = 
'<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v13="https://bingads.microsoft.com/Customer/v13">
<soapenv:Header>
   <v13:DeveloperToken>{0}</v13:DeveloperToken>
   <v13:AuthenticationToken>{1}</v13:AuthenticationToken>
</soapenv:Header>
<soapenv:Body>
   <v13:GetUserRequest>
      <v13:UserId xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
   </v13:GetUserRequest>
</soapenv:Body>
</soapenv:Envelope>' -f $developerToken, $accessToken

$headers = @{"SOAPAction" = "GetUser"}

$uri = "https://clientcenter.api.bingads.microsoft.com/Api/CustomerManagement/v13/CustomerManagementService.svc"
$response = Invoke-WebRequest $uri -Method post -ContentType 'text/xml' -Body $getUserRequest -Headers $headers
Write-Output $response.Content