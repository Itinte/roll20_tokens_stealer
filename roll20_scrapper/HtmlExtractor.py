import re

class HtmlExtractor:
    def __init__(self, positivePatternList, negativePatternList = None, matchPostProcessLambda = lambda x: x):
        self.matchPostProcessLambda = matchPostProcessLambda
        self.positivePatternList = []
        self.negativePatternList = []
        for pPattern in positivePatternList:
            self.positivePatternList.append(re.compile(pPattern))
        if (negativePatternList is not None):
            for nPattern in negativePatternList :
                self.negativePatternList.append(re.compile(nPattern))

    def match(self, html):
        html = str(html)
        if self.negativePatternList is not None:
            for negativePattern in self.negativePatternList:
                if (len(negativePattern.findall(html))>0):
                    return False
        for positivePatternList in self.positivePatternList:
            if (len(positivePatternList.findall(html))==0):
                return False
        return self.matchPostProcessLambda(html)
