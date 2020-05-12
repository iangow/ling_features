#!/usr/bin/env python3
import re, json
from nltk.tokenize import wordpunct_tokenize
import pandas as pd

# Word list from draft of Kothari, Li and Short (2009)
word_list = {
	'market': ['market', 'marketplace', 'environment', 'segment', 'sector'],
	'competition': ['market', 'marketplace', 'environment', 'customer', 'channel', 'value',
		'first-mover', 'technology', 'alliance', 'partnership', 'venture',
		'regulation', 'litigation'],
	'industry_structure': ['industry', 'entrant', 'supplier', 'buyer', 'substitute',
		'scale', 'product', 'brand', 'switching', 'capital', 'access', 'cost',
		'rivalry', 'capacity', 'concentration', 'exit', 'barrier', 'price', 'profit',
		'quality', 'input', 'volume', 'purchase', 'integration',
		'power'],
	'strategic_intent': ['strategy', 'strategic', 'value', 'sales', 'revenue',
		'share', 'profit', 'profitability', 'product', 'service', 'lead',
		'leader', 'quality', 'customer', 'buyer', 'growth', 'opportunity',
		 'risk', 'resource'],
	'innovation_and_r_d': ['research and development', 'r&d', 'patent', 'discovery',
		'license', 'licensing', 'regulation', 'regulatory', 'trial', 'monitor',
		'innovate', 'innovation', 'competence'],
	'mode_of_entry': ['entry', 'cost', 'business', 'complementary', 'green-field',
		'venture', 'investment', 'capital', 'solution', 'price'],
	'business_model': ['model', 'best', 'lowest', 'low', 'highest', 'high',
		 'supplier', 'distribution'],
	'partnerships': ['partner', 'alliance', 'merger', 'acquisition', 'joint',
		'venture', 'relationship', 'equity', 'asset'],
	'leadership': ['leader', 'leadership', 'record', 'value', 'culture',
		'responsibility', 'goal', 'objective'],
	'management_quality': ['management', 'quality', 'best', 'proven',
		'experience', 'teamwork'],
	'governance': ['recruitment', 'development', 'governance', 'corporate',
		 'board', 'incentive', 'owner', 'ownership', 'compensation'],
	'disclosure': ['disclosure', 'transparent', 'transparency', 'information',
		'audit', 'auditing', 'oversight', 'assurance', 'regulation', 'mandate',
		'mandated'],
	'measures': ['up', 'down', 'better', 'worse', 'recover', 'advance',
		'advancing', 'progress', 'progressing', 'expand', 'expanding', 'improve',
		 'improving', 'reduce', 'reducing', 'reduction', 'decline', 'declining',
		'retain', 'retention', 'profit', 'profitability', 'feedback', 'scorecard',
			 'growth', 'growing', 'performance', 'projected', 'projections'],
	'customer': ['customer', 'satisfaction', 'feedback', 'trust'],
	'brand': ['brand', 'image', 'name', 'trademark', 'recognition', 'stretch',
		'quality', 'awareness'],
	'media': ['radio', 'television', 'newspaper', 'internet', 'promotion',
		'media spend', 'announcements', 'release', 'media budget'],
	'advertising': ['advertising', 'ad', 'direct', 'channel', 'advertising', 'spend',
		'ad spend', 'advertising allocation', 'budget', 'ad budget'],
	'corporate_image': ['corporate image', 'reputation', 'integrity', 'community',
		'trust', 'trusted name', 'confidence', 'durability', 'strength', 'character'],
	'financial_performance': ['gross', 'net', 'return on investment', 'return on sales',
		'return on assets', 'return on equity', 'ROI', 'ROA', 'ROE', 'profit',
		'earnings', 'margin', 'capital', 'debt', 'sales', 'EBITDA', 'ratings',
		 'leverage', 'valuation', 'cost of capital'],
	'forecasting': ['forecast', 'forecasting', 'cash flow', 'prospectus', 'quarterly'],
	'insider_stock_transactions': ['insider buy', 'insider sell'],
	'regulation': ['regulation', 'federal', 'state', 'securities and exchange', 'commission',
		 'commerce', 'legislation', 'congress', 'law', 'legal', 'hearings',
		 'enacted', 'pending', 'sec', 'medicare', 'medicaid', 'FDA'],
	'special_interest_groups': ['lobby', 'lobbyists', 'special', 'interest', 'expert',
		'testimony', 'industry', 'watchdog', 'consumer rights', 'patient rights']
		}

def kls_domains(raw_text):

	lower_text = raw_text.lower()

	domains = [domain for domain in word_list.keys()
		for term in word_list[domain] if re.search(term, lower_text)]
	return list(set(domains))

def kls_domains_ind(raw_text):

    domains = word_list.keys()
    domain_list = kls_domains(raw_text)

    return json.dumps({domain: domain in domain_list for domain in domains})

def expand_json(df, col):
    return pd.concat([df.drop([col], axis=1),
                      df[col].map(lambda x: json.loads(x)).apply(pd.Series)], axis=1)

if __name__=="__main__":

    text = "I think you spent a little bit of time talking about AdSense for Content, " + \
            "but also in my mind kind of along the lines of what seemed to be from a consumer" + \
            " standpoint, material product innovations. You have had GMail I guess in beta for" + \
            " getting close to a year and I think Froogle, too. I was wondering if you can help us " + \
            "understand a), I guess those are all in the Google website's portion of the business or maybe " + \
            "AdSense for Content is not. Can you kind of just help us understand where those are in the " + \
            "income statement, and to what degree those are contributing to the Company's growth " + \
            "today versus six months ago, or even what percentage of today's revenue is coming from" + \
            " those new products? "

    print(kls_domains_ind(text))
