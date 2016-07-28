#!/usr/bin/env python

import sys
import re

#global variables
topic_id_list = []
topic_to_word_frequency = {}
topic_to_word_frequency_sum = {}
topic_probability = {}
vocabulary = []
T = 0
E = 0
unimportant = ['its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who',
             'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'should', 'now''yourself',
	      'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it',
             'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
             'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
	    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the',
             'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
             'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below',
             'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
             'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
             'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same']

fp = open('output', 'w')

def computeWordProbability(word, topic):
	topic_word_freq = topic_to_word_frequency[topic]
	freq = float(0)
	if word in topic_word_freq:
		freq = float(topic_word_freq[word])
	return (freq + 1) / float(topic_to_word_frequency_sum[topic])

def compareTopicRelevance(topic1, topic2):
	key1 = topic1.keys()[0]
	key2 = topic2.keys()[0]
	if topic1[key1] > topic2[key2]:
		return -1
	elif topic1[key1] == topic2[key2]:
		if key1 < key2:
			return -1
		else:
			return 1
	else:
		return 1	

#apply Bayes Rule to compute the probabilities of relevance for all topicIDs for the query
def computeRelevance(query):
	topics_to_relevance = []
	for topic in topic_id_list:
		topic_prob = {}
		prob = float(1)
		words = query.split(" ")
		for word in words:
			if word not in unimportant:
				prob *= (computeWordProbability(word, topic) * topic_probability[topic])
		topic_prob[topic] = prob
		topics_to_relevance.append(topic_prob)
	topics_to_relevance.sort(compareTopicRelevance)
	return topics_to_relevance		

#get topicIDs in decreasing order of relevance for the query and print top 10 
def getTopTenRelevantTopics(query):
	relevance_ordered_topics = computeRelevance(query)
	count = 0		
	for topic in relevance_ordered_topics:
		if count == 10 :
			break
		key = topic.keys()[0]
		#sys.stdout.write(str(key) + " ")
		fp.write(str(key) + " ")
		count += 1
	#sys.stdout.write("\n")	
	fp.write("\n")

def parseInput(input_data):
	global vocabulary, topic_to_word_frequency 
	T = int(input_data[0].split(" ")[0])
	E = int(input_data[0].split(" ")[1])
	index = 1
	topic_to_query_count = {}
	while index < ((2 * T) + 1):
		topic_line = input_data[index].split(" ")
		#get number of topics for query
		num_topics = int(topic_line[0])
		topics = []
		#build list of topics
		for i in range(1, num_topics + 1):
			topics.append(int(topic_line[i]))
		for topic in topics:
			if topic not in topic_id_list:
				topic_id_list.append(topic)

		#build vocabulary
		words = input_data[index + 1].split(" ")
		words = [re.sub('[?]+', '', word) for word in words]
		for word in words:
			if word not in vocabulary and word not in unimportant:
				vocabulary.append(word)
	
		#build topic to query count map
		for topic in topics:
			if topic in topic_to_query_count:
				topic_to_query_count[topic] = topic_to_query_count[topic] + 1
			else:
				topic_to_query_count[topic] = 1

		#build topic to word frequency map
		for topic in topics:
			topic_to_words = {}
			if topic in topic_to_word_frequency:
				topic_to_words = topic_to_word_frequency[topic]				 
			for word in words:
				if word not in unimportant:
					if word in topic_to_words:
						topic_to_words[word] = topic_to_words[word] + 1
					else:
						topic_to_words[word] = 1
				topic_to_word_frequency[topic] = topic_to_words

		index += 2

	#compute total word frequency for all topics
	for topic in topic_id_list:
		total = 0
		words = topic_to_word_frequency[topic]
		for word in words:
			total += words[word]
		total += len(vocabulary)
		topic_to_word_frequency_sum[topic] = total
	
	#compute topic probability
	for topic in topic_id_list:
		topic_probability[topic] = float((topic_to_query_count[topic])) / float(T)

	#extract the questions to be classified
	queries = []
	for query_count in range(E):
		query = input_data[index]
		#query = re.sub('[^\w\s]+', '', query)
		query = re.sub('[?]+', '', query)
		queries.append(query)
		index += 1
	return queries

def main():
	#input_data = sys.stdin.readlines()
	#if len(sys.argv) != 2:
	#	print "Usage: python labeler.py input_data_file"
	#	return
	input_data = open(sys.argv[1]).read().split("\n")
  	input_data = [x.rstrip() for x in input_data]
	input_data = [x.lower() for x in input_data]	
	queries = parseInput(input_data)	
	for query in queries:
		getTopTenRelevantTopics(query)
	fp.close()
if __name__ == "__main__" :
	main()
