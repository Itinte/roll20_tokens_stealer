from HtmlExtractor import HtmlExtractor

class HtmlParser:
    def __init__(self, htmlExtractorsList):
        self.html_extractors = htmlExtractorsList
    
    def parse(self, html_page):
        html_extractor_results = dict()
        for extractor in self.html_extractors:
            html_extractor_results[extractor] = []
        for line in html_page:
            if len(line)>0:
                for extractor in self.html_extractors:
                    _extractor_line_result = extractor.match(line)
                    if _extractor_line_result != False:
                        html_extractor_results[extractor].append(_extractor_line_result)
        return html_extractor_results
