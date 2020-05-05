import win32com.client
import time

# StockChart : 주식, 업종, ELW의 차트데이터를 수신합니다
def CheckVolumn(instStockChart, code):
    # SetInputValue
    # 0 - 종목코드(string)
    # 1 - 요청구분(char)
    # 2 - 요청종료일(ulong)
    # 3 - 요청시작일(ulong)
    # 4 - 요청개수(ulong)
    # 5 - 필드(long or long array)
    # 6 - 차트구분(char)
    # 9 - 수정주가(char)
    instStockChart.SetInputValue(0, code)
    instStockChart.SetInputValue(1, ord('2'))
    instStockChart.SetInputValue(4, 60)
    # 필드값 두번째 인자
    # 0: 날짜(ulong)
    # 1: 시간(long) - hhmm
    # 2: 시가(long or float)
    # 3: 고가(long or float)
    # 4: 저가(long or float)
    # 5: 종가(long or float)
    # 8: 거래량(ulong or ulonglong)
    instStockChart.SetInputValue(5, 8)
    instStockChart.SetInputValue(6, ord('D'))
    instStockChart.SetInputValue(9, ord('1'))

    # BlockRequest
    instStockChart.BlockRequest()

    # GetData
    volumes = []
    # 수신 데이터 갯수
    numData = instStockChart.GetHeaderValue(3)
    for i in range(numData):
        volume = instStockChart.GetDataValue(0, i)
        volumes.append(volume)

    # 최근 59일간 평균
    averageVolume = (sum(volumes) - volumes[0]) / (len(volumes) -1)

    if(volumes[0] > averageVolume * 10):
        return 1
    else:
        return 0

if __name__ == "__main__":
    instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
    instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
    # 유가증권시장 코드 리스트
    codeList = instCpCodeMgr.GetStockListByMarket(1)

    buyList = []
    for code in codeList:
        if instCpCodeMgr.GetStockSectionKind(code) != 1:
            continue
        if CheckVolumn(instStockChart, code) == 1:
            buyList.append(code)
            print(code, instCpCodeMgr.CodeToName(code))
            time.sleep(1)