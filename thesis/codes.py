ssa_country_codes = [
    "AGO", "BEN", "BWA", "BFA", "BDI", "CPV", "CMR", "CAF", "TCD", "COM", "COG",
    "COD", "DJI", "GNQ", "ERI", "SWZ", "ETH", "GAB", "GMB", "GHA", "GIN", "GNB",
    "CIV", "KEN", "LSO", "LBR", "LBY", "MDG", "MWI", "MLI", "MRT", "MUS", "MOZ",
    "NAM", "NER", "NGA", "RWA", "STP", "SEN", "SYC", "SLE", "SOM", "ZAF", "SSD",
    "SDN", "TZA", "TGO", "UGA", "ZMB", "ZWE"
]

indicator_codes = [
    "NY.GDP.MKTP.KD.ZG",  # GDP growth (annual %)
    "NY.GDP.PCAP.KD.ZG",  # GDP per capita growth (annual %)
    "SL.UEM.TOTL.ZS",  # Unemployment, total (% of total labor force)
    "FP.CPI.TOTL.ZG",  # Inflation, consumer prices (annual %)
    "NE.TRD.GNFS.ZS",  # Trade (% of GDP)
    "GC.TAX.TOTL.GD.ZS",  # Tax revenue (% of GDP)
    "NE.CON.PRVT.PC.KD.ZG",  # Final consumption expenditure, etc. (annual % growth)
    "SP.POP.GROW",  # Population growth (annual %)
    "NY.GDS.TOTL.ZS",  # Gross domestic savings (% of GDP)
    "NE.EXP.GNFS.ZS",  # Exports of goods and services (% of GDP)
    "NE.IMP.GNFS.ZS",  # Imports of goods and services (% of GDP)
    "NV.AGR.TOTL.ZS",  # Agriculture, forestry, and fishing, value added (% of GDP)
    "NV.IND.TOTL.ZS",  # Industry (including construction), value added (% of GDP)
    "NV.SRV.TOTL.ZS",  # Services, value added (% of GDP)
    "SL.GDP.PCAP.EM.KD",  # GDP per person employed (constant 2017 PPP $)
    "GC.DOD.TOTL.GD.ZS",  # Central government debt, total (% of GDP)
    "FS.AST.PRVT.GD.ZS",  # Domestic credit to private sector (% of GDP)
    "SH.XPD.GHED.GD.ZS",  # Current health expenditure (% of GDP)
    # "ER.H20.INTR.PC",       # Fresh water
    "EG.ELC.ACCS.ZS",  # Access to electricity
    "SP.POP.DPND"  # Age dependency ratio

]


updated_indicator_dict = {
    "NY.GDP.PCAP.KD.ZG": "GDP per capita growth (annual %)",
    "FP.CPI.TOTL.ZG": "Inflation, consumer prices (annual %)",
    "SP.POP.GROW": "Population growth (annual %)",
    "NV.AGR.TOTL.ZS": "Agriculture, forestry, and fishing, value added (% of GDP)",
    "ER.H2O.INTR.PC": "Access to fresh water",
    "EG.ELC.ACCS.ZS": "Access to electricity",
    "GC.NFN.TOTL.GD.ZS": "Net investment in nonfinacial assets",
    "NY.TTF.GNFS.KN": "Terms of trade adjustment (constant LCU)",
    "SP.POP.DPND": "Age dependency ratio",
    "NE.TRD.GNFS.ZS": "Trade (% of GDP)",
    "IC.TAX.TOTL.CP.ZS": "Total tax and contribution rate (% of profit)",
    "PA.NUS.PPPC.RF": "Price level ratio of PPP conversion factor (GDP) to market exchange rate",
    "IQ.CPA.TRAN.XQ": "CPIA transparency, accountability, and corruption in the public sector rating (1=low to 6=high)",
    "SE.ADT.LITR.ZS": "Literacy rate total (% of people aged 15 and above)",
    "NV.IND.TOTL.ZS": "Industry (including construction), value added (% of GDP)",
    "NV.SRV.TOTL.ZS": "Services, value added (% of GDP)",
    "SL.UEM.TOTL.ZS": "Unemployment, total (% of total labor force)",
    "GB.XPD.RSDV.GD.ZS": "R&D expenditure (% of GDP)"

}

indicator_dict = {
    "NY.GDP.MKTP.KD.ZG": "GDP growth (annual %)",
    "NY.GDP.PCAP.KD.ZG": "GDP per capita growth (annual %)",
    "SL.UEM.TOTL.ZS": "Unemployment, total (% of total labor force)",
    "FP.CPI.TOTL.ZG": "Inflation, consumer prices (annual %)",
    "NE.TRD.GNFS.ZS": "Trade (% of GDP)",
    "GC.TAX.TOTL.GD.ZS": "Tax revenue (% of GDP)",
    "NE.CON.PRVT.PC.KD.ZG": "Final consumption expenditure, etc. (annual % growth)",
    "SP.POP.GROW": "Population growth (annual %)",
    "NY.GDS.TOTL.ZS": "Gross domestic savings (% of GDP)",
    "NE.EXP.GNFS.ZS": "Exports of goods and services (% of GDP)",
    "NE.IMP.GNFS.ZS": "Imports of goods and services (% of GDP)",
    "NV.AGR.TOTL.ZS": "Agriculture, forestry, and fishing, value added (% of GDP)",
    "NV.IND.TOTL.ZS": "Industry (including construction), value added (% of GDP)",
    "NV.SRV.TOTL.ZS": "Services, value added (% of GDP)",
    "SL.GDP.PCAP.EM.KD": "GDP per person employed (constant 2017 PPP $)",
    "GC.DOD.TOTL.GD.ZS": "Central government debt, total (% of GDP)",
    "FS.AST.PRVT.GD.ZS": "Domestic credit to private sector (% of GDP)",
    "SH.XPD.GHED.GD.ZS": "Current health expenditure (% of GDP)",
    "ER.H20.INTR.PC": "Access to fresh water",
    "EG.ELC.ACCS.ZS": "Access to electricity",
    "SP.POP.DPND": "Age dependency ratio",
    "SE.ADT.LITR.ZS": "Literacy rate total (% of people aged 15 and above)",
    "IQ.CPA.TRAN.XQ": "CPIA transparency, accountability, and corruption in the public sector rating (1=low to 6=high)",
    "PA.NUS.PPPC.RF": "Price level ratio of PPP conversion factor (GDP) to market exchange rate",
    "IC.TAX.TOTL.CP.ZS": "Total tax and contribution rate (% of profit)",
    "GB.XPD.RSDV.GD.ZS": "R&D expenditure (% of GDP)"


}

indicator_dict_large = {
    "GDP per capita (constant 2010 US$)": "NY.GDP.PCAP.KD",
    "GDP growth (annual %)": "NY.GDP.MKTP.KD.ZG",
    "Inflation, consumer prices (annual %)": "FP.CPI.TOTL.ZG",
    "Unemployment, total (% of total labor force)": "SL.UEM.TOTL.ZS",
    "Gross capital formation (% of GDP)": "NE.GDI.TOTL.ZS",
    "Gross savings (% of GDP)": "NY.GNS.ICTR.GN.ZS",
    "Exports of goods and services (% of GDP)": "NE.EXP.GNFS.ZS",
    "Imports of goods and services (% of GDP)": "NE.IMP.GNFS.ZS",
    "Current account balance (% of GDP)": "BN.CAB.XOKA.GD.ZS",
    "Total reserves (includes gold, current US$)": "FI.RES.TOTL.CD",
    "Total debt service (% of exports of goods, services and primary income)": "DT.TDS.DECT.EX.ZS",
    "Gross domestic savings (% of GDP)": "NY.GDS.TOTL.ZS",
    "Population growth (annual %)": "SP.POP.GROW",
    "Urban population growth (annual %)": "SP.URB.GROW",
    "Life expectancy at birth, total (years)": "SP.DYN.LE00.IN",
    "Mortality rate, under-5 (per 1,000 live births)": "SH.DYN.MORT",
    "Access to electricity (% of population)": "EG.ELC.ACCS.ZS",
    "CO2 emissions (metric tons per capita)": "EN.ATM.CO2E.PC",
    "Renewable energy consumption (% of total final energy consumption)": "EG.FEC.RNEW.ZS",
    "Foreign direct investment, net inflows (% of GDP)": "BX.KLT.DINV.WD.GD.ZS",
    "Tax revenue (% of GDP)": "GC.TAX.TOTL.GD.ZS",
    "Government expenditure (% of GDP)": "GC.XPN.TOTL.GD.ZS",
    "Domestic credit to private sector (% of GDP)": "FS.AST.DOMS.GD.ZS",
    "Lending interest rate (%)": "FR.INR.LEND",
    "Deposit interest rate (%)": "FR.INR.DPST",
    "Market capitalization of listed domestic companies (% of GDP)": "CM.MKT.LCAP.GD.ZS",
    "Trade (% of GDP)": "NE.TRD.GNFS.ZS",
    "Foreign direct investment, net outflows (% of GDP)": "BM.KLT.DINV.WD.GD.ZS",
    "Gross domestic product (constant 2010 US$)": "NY.GDP.MKTP.KD",
    "Gross domestic product (current US$)": "NY.GDP.MKTP.CD",
    "Gross domestic product, PPP (constant 2017 international $)": "NY.GDP.MKTP.PP.KD",
    "Gross domestic product, PPP (current international $)": "NY.GDP.MKTP.PP.CD",
    "Gross value added at basic prices (GVA) (constant 2010 US$)": "NY.GVA.MKTP.KD",
    "Gross value added at basic prices (GVA) (current US$)": "NY.GVA.MKTP.CD",
    "Gross national income (GNI) (constant 2010 US$)": "NY.GNP.MKTP.KD",
    "Gross national income (GNI) (current US$)": "NY.GNP.MKTP.CD",
    "Gross national income, PPP (constant 2017 international $)": "NY.GNP.MKTP.PP.KD",
    "Gross national income, PPP (current international $)": "NY.GNP.MKTP.PP.CD",
    "Final consumption expenditure (constant 2010 US$)": "NE.CON.TOTL.KD",
    "Final consumption expenditure (current US$)": "NE.CON.TOTL.CD",
    "Foreign exchange reserves (excluding gold) (current US$)": "FI.RES.XGLD.CD",
    "International tourism, receipts (% of total exports)": "ST.INT.RCPT.XP.ZS",
    "International tourism, receipts (current US$)": "ST.INT.RCPT.CD",
    "Portfolio investment, net (BoP, current US$)": "BN.KLT.PTXL.CD",
    "Public and publicly guaranteed debt service (% of exports of goods, services and primary income)": "DT.TDS.DPPG.XP.ZS",
    "Research and development expenditure (% of GDP)": "GB.XPD.RSDV.GD.ZS",
    "Agriculture, forestry, and fishing, value added (% of GDP)": "NV.AGR.TOTL.ZS",
    "Industry (including construction), value added (% of GDP)": "NV.IND.TOTL.ZS",
    "Services, value added (% of GDP)": "NV.SRV.TOTL.ZS",
    "Gross fixed capital formation (% of GDP)": "NE.GDI.FTOT.ZS",
   
}

business_indicators = {
    "Ease of doing business index (1=most business-friendly regulations)": "IC.BUS.EASE.XQ",
    "Dealing with construction permits (score)": "IC.CNST.DURS",
    "Getting electricity (score)": "IC.ELC.ACSZ",
    "Registering property (score)": "IC.PRP.PROC.NO",
    "Getting credit (score)": "IC.CRD.SCOR",
    "Protecting minority investors (score)": "IC.PMI.INVX",
    "Paying taxes (score)": "IC.TAX.TOTL.SC",
    "Trading across borders (score)": "IC.TAX.TOTL.SC",
    "Enforcing contracts (score)": "IC.LGL.CRED.SC",
    "Resolving insolvency (score)": "IC.ISV.SCOR",
    "Labor tax and contributions (% of commercial profits)": "IC.TAX.LABR.CP.ZS",
    "Getting electricity: time (days)": "IC.ELC.TIME",
    "Getting electricity: cost (% of income per capita)": "IC.ELC.COST.PC.ZS",
    "Registering property: time (days)": "IC.PRP.TIME",
    "Registering property: cost (% of property value)": "IC.PRP.COST.PC.ZS",
    "Enforcing contracts: time (days)": "IC.LGL.DURS",
    "Enforcing contracts: cost (% of claim)": "IC.LGL.COST.PC.ZS",
    "Resolving insolvency: time (years)": "IC.ISV.DURS",
    "Resolving insolvency: cost (% of estate)": "IC.ISV.COST.PC.ZS",
    "Resolving insolvency: recovery rate (cents on the dollar)": "IC.ISV.RECRT"
}

switched_dict_business = {value: key for key, value in business_indicators.items()}

ease_of_business = ["Score-Starting a business", "Score-Dealing with construction permits (DB06-15 methodology)",
                    "Score-Getting electricity (DB16-20 methodology)",
                    "Score-Registering property (DB05-15 methodology)",
                    "Getting Credit total score (DB15-20 methodology)",
                    "Score-Protecting minority investors (DB15-20 methodology)",
                    "Score-Paying taxes (DB17-20 methodology)", "Score-Trading across borders (DB16-20 methodology)",
                    "Score-Enforcing contracts (DB17-20 methodology)"]

ease_of_business_weights = {"Score-Starting a business": 0.2,
                            "Score-Dealing with construction permits (DB06-15 methodology)": 0.1,
                            "Score-Getting electricity (DB16-20 methodology)": 0.15,
                            "Score-Registering property (DB05-15 methodology)": 0.1,
                            "Getting Credit total score (DB15-20 methodology)": 0.15,
                            "Score-Protecting minority investors (DB15-20 methodology)": 0.05,
                            "Score-Paying taxes (DB17-20 methodology)": 0.1,
                            "Score-Trading across borders (DB16-20 methodology)": 0.1,
                            "Score-Enforcing contracts (DB17-20 methodology)": 0.05}

indicators_new = {
    "NY.GDP.PCAP.KD.ZG": "GDP.growth",
    "SL.UEM.TOTL.ZS": "Unemployment, total (% of total labor force)",
    "SP.POP.DPND": "Age dependency ratio",
    "SE.ADT.LITR.ZS": "Literacy rate total (% of people aged 15 and above)",
    "GC.DOD.TOTL.GD.ZS": "Central government debt, total (% of GDP)",
    "GB.XPD.RSDV.GD.ZS": "R&D expenditure (% of GDP)",
    "IQ.CPA.TRAN.XQ": "CPIA transparency, accountability, and corruption in the public sector rating (1=low to 6=high)",
    "NV.SRV.TOTL.ZS": "Services, value added (% of GDP)",
    "NV.IND.TOTL.ZS": "Industry (including construction), value added (% of GDP)",
    "BX.KLT.DINV.CD.WD": "Foreign direct investment, net inflows (BoP, current US$)",
    "EG.ELC.ACCS.ZS": "Access to electricity",
    "FS.AST.PRVT.GD.ZS": "Domestic credit to private sector (% of GDP)",
    "NE.TRD.GNFS.ZS": "Trade (% of GDP)",
    "NY.TTF.GNFS.KN": "Terms of trade adjustment (constant LCU)",
    "NE.EXP.GNFS.ZS": "Exports of goods and services (% of GDP)",

}

