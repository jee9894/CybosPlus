# 산업종 리스트
# 001 종합주가지수
# 002 대형(시가총액)
# 003 중형(시가총액)
# 004 소형(시가총액)
# 005 음식료품
# 006 섬유,의복
# 007 종이,목재
# 008 화학
# 009 의약품
# 010 비금속광물
# 011 철강,금속
# 012 기계
# 013 전기,전자
# 014 의료정밀
# 015 운송장비
# 016 유통업
# 017 전기가스업
# 018 건설업
# 019 운수창고
# 020 통신업
# 021 금융업
# 022 은행
# 024 증권
# 025 보험
# 026 서비스업
# 027 제조업

import win32com.client
import time

instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
instMarketEye = win32com.client.Dispatch("CpSysDib.MarketEye")

industryCodeList = instCpCodeMgr.GetIndustryList()

for industryCode in industryCodeList:
    iCode = int(industryCode)
    if iCode > 100:
        break

    # Get PER
    targetCodeList = instCpCodeMgr.GetGroupCodeList(iCode+1)
    # 한번에 요청할 수 있는 종목수 최대 200개
    if len(targetCodeList) > 200:
        targetCodeList = targetCodeList[:200]
    instMarketEye.SetInputValue(0, 67)
    instMarketEye.SetInputValue(1, targetCodeList)

    # BlockRequest
    instMarketEye.BlockRequest()

    numStock = instMarketEye.GetHeaderValue(2)
    sumPer = 0

    for i in range(numStock):
        sumPer += instMarketEye.GetDataValue(0, i)

    if numStock != 0:
        print("Average PER Of", instCpCodeMgr.GetIndustryName(industryCode), ":", sumPer / numStock)
    else :
        print(instCpCodeMgr.GetIndustryName(industryCode), "has no SubObject")
    time.sleep(1)