class AlisonApi:
    def __init__(self, session):
        self.session = session

    async def get_all_bill_summaries(self, limit=None):
        count = await self.get_bill_count()
        if limit is not None and count > limit:
            count = limit
        result = []
        for offset in range(0, count, PER_PAGE):
            result += await self.get_bill_summaries_page(limit=PER_PAGE, offset=offset)
        return result

    async def get_bill_count(self):
        async with self.session.post(
            GRAPHQL_URL, json={"query": INSTRUMENT_COUNT_QUERY, "variables": {}}
        ) as response:
            data = await response.json()
        return data["data"]["allInstrumentOverviewsCount"]

    async def get_bill_summaries_page(self, limit, offset):
        query = INSTRUMENT_SUMMARY_QUERY.replace("limit:15", f"limit:{limit}").replace(
            "offset:0", f"offset:{offset}"
        )
        async with self.session.post(
            GRAPHQL_URL, json={"query": query, "variables": {}}
        ) as response:
            data = await response.json()
        return data["data"]["allInstrumentOverviews"]


PER_PAGE = 15
GRAPHQL_URL = "https://alison.legislature.state.al.us/graphql"
INSTRUMENT_COUNT_QUERY = """{
								allInstrumentOverviewsCount(instrumentType:"B", instrumentNbr:"", body:"", sessionYear:"2025", sessionType:"2025 Regular Session", assignedCommittee:"", status:"", currentStatus:"", subject:"", instrumentSponsor:"", companionInstrumentNbr:"", effectiveDateCertain:"", effectiveDateOther:"", firstReadSecondBody:"", secondReadSecondBody:"", direction:"ASC"orderBy:"InstrumentNbr"companionReport:"", search:"" customFilters: {})
							}"""
INSTRUMENT_SUMMARY_QUERY = """{allInstrumentOverviews(instrumentType:"B", instrumentNbr:"", body:"", sessionYear:"2025", sessionType:"2025 Regular Session", assignedCommittee:"", status:"", currentStatus:"", subject:"", instrumentSponsor:"", companionInstrumentNbr:"", effectiveDateCertain:"", effectiveDateOther:"", firstReadSecondBody:"", secondReadSecondBody:"", direction:"ASC"orderBy:"InstrumentNbr"limit:15 offset:0  search:"" customFilters: {}companionReport:"", ){ ID,SessionYear,InstrumentNbr,InstrumentSponsor,SessionType,Body,Subject,ShortTitle,AssignedCommittee,PrefiledDate,FirstRead,CurrentStatus,LastAction,ActSummary,ViewEnacted,CompanionInstrumentNbr,EffectiveDateCertain,EffectiveDateOther,InstrumentType }}"""
