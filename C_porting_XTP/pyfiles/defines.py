#!/usr/bin/python
#! -*- encoding=utf-8 -*-

import os
import re
import shutil
import time

class_pattern_spi = re.compile('class\s(\w+)\s')
class_pattern_api = re.compile('class\s\w+\s(\w+)\s')
method_pattern = re.compile("virtual\s(\w+)\s(\w+)\((.*)\)")

COMMON_H = 'common_macro.h'

XTP_INCLUDE_PATH = '../include/XTP'

output_api_dir = '../include/CXTPApi'

output_dir = '../src/Platform/CXTPApiImpl'

output_wrapper_go_dir = '../../go_src/xtp_wrapper'

output_go_package = 'queue'

output_queues_go_dir = '../../go_src/' + output_go_package

others_dir = '../others'

output_def_go_file = 'xtp_message.go'

XTP_H_Base = 'XTP'

XTPCApi_H_Base = 'CXTPApi'

LC_XTP_API = 'LC_XTP_API'

LC_PREFIX = 'LC'

FN = 'fn'

GoPrefix = 'Go'

LC_SUFFIX = 'Impl'

FTDC_STR = 'Ftdc'

REG_PREFIX = 'Register'

RegisterSpi = 'RegisterSpi'

pApi_name = 'pLC_Api'

pSpi_name = 'pLC_Spi'

bIsUsingUdp = 'bIsUsingUdp'

bIsMulticast = 'bIsMulticast'

client_id = 'client_id'
save_file_path = 'save_file_path'
log_level = 'log_level'

VOID_PTR = '(unsigned long long int)this'

Extern_Ptr_Param = 'unsigned long long int spiPtr'

char_arr_pattern = re.compile('typedef\schar\s([A-Za-z]{1,}Type);')
enum_arr_pattern = re.compile('enum\s([A-Za-z_]{1,})')

output_util_go_file = 'xtp_convert_util.go'

typedefStructLst = [ 'XTPRI', 'XTPTPI', 'XTPST', 'XTPMD', 'XTPOB', 'XTPTBT', 'XTPQSI', 'XTPQueryOrderRsp', 'XTPQueryOrderRsp', 'XTPQueryTradeRsp' ]

md_concern_list = []
trader_concern_list = []

#md_concern_list = [ 'Go_quote_apiOnSubMarketData', 'Go_quote_apiOnMarketData', 'Go_quote_apiOnSubOrderBook', 'Go_quote_apiOnOrderBook' ]
trader_concern_list = [ 'Go_trader_apiOnDisconnected', 'Go_trader_apiOnOrderEvent', 'Go_trader_apiOnTradeEvent', 
    'Go_trader_apiOnQueryOrder', 'Go_trader_apiOnQueryTrade', 'Go_trader_apiOnQueryPosition', 'Go_trader_apiOnQueryAsset' ]

trader_concern_list = [ 'Go_trader_apiOnDisconnected' ]

typedefedStructs = {
    'XTPRI': 'XTPRspInfoStruct',
    'XTPST': 'XTPSpecificTickerStruct',
    'XTPMD': 'XTPMarketDataStruct',
    'XTPQSI': 'XTPQuoteStaticInfo',
    'XTPOB': 'OrderBookStruct',
    'XTPTBT': 'XTPTickByTickStruct',
    'XTPTPI': 'XTPTickerPriceInfo',
    'XTPRI': 'XTPRspInfoStruct',
    'XTPQueryOrderRsp': 'XTPOrderInfo',
    'XTPQueryTradeRsp': 'XTPTradeReport',
    'XTPFundTransferLog': 'XTPFundTransferNotice',
    'XTPFundTransferAck': 'XTPFundTransferNotice',
    'XTPQueryETFBaseRsp': 'XTPQueryETFBaseRsp',
    'XTPCrdDebtInfo': 'XTPCrdDebtInfo',
    'XTPCrdFundInfo': 'XTPCrdFundInfo',
    'XTPClientQueryCrdDebtStockReq': 'XTPClientQueryCrdDebtStockReq',
    'XTPCrdDebtStockInfo': 'XTPCrdDebtStockInfo',
    'XTPClientQueryCrdPositionStockReq': 'XTPClientQueryCrdPositionStockReq',
    'XTPClientQueryCrdPositionStkInfo': 'XTPClientQueryCrdPositionStkInfo',
}

untypedefedStructs = {
    'XTPMarketDataStockExData': '',
    'XTPMarketDataOptionExData': '',
    'XTPTickByTickEntrust': '',
    'XTPTickByTickTrade': '',
    'XTPOrderInsertInfo': '',
    'XTPOrderCancelInfo': '',
    'XTPQueryOrderReq': '',
    'XTPQueryOrderByPageReq': '',
    'XTPQueryReportByExecIdReq': '',
    'XTPQueryTraderReq': '',
    'XTPQueryTraderByPageReq': '',
    'XTPQueryAssetRsp': '',
    'XTPQueryStkPositionRsp': '',
    'XTPQueryFundTransferLogReq': '',
    'XTPQueryStructuredFundInfoReq': '',
    'XTPStructuredFundInfo': '',
    'XTPQueryETFBaseReq': '',
    'XTPQueryETFComponentRsp': '',
    'XTPQueryIPOTickerRsp': '',
    'XTPQueryIPOQuotaRspV1': '',
    'XTPQueryIPOQuotaRsp': '',
    'XTPQueryOptionAuctionInfoReq': '',
    'XTPQueryOptionAuctionInfoRsp': '',
    'XTPCrdCashRepayRsp': '',
    'XTPCrdCashRepayInfo': '',
    'XTPFundTransferReq': '',
}

typedefedEnums = {
}

untypedefedEnums = {
}

fields = dict()
