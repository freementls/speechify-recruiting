#!/usr/bin/env python3
"""
SSML (Speech Synthesis Markup Language) is a subset of XML specifically
designed for controlling synthesis. You can see examples of how the SSML
should be parsed in the unit tests below.
"""

#
# DO NOT USE CHATGPT, COPILOT, OR ANY AI CODING ASSISTANTS.
# Conventional auto-complete and Intellisense are allowed.
#
# DO NOT USE ANY PRE-EXISTING XML PARSERS FOR THIS TASK - lxml, ElementTree, etc.
# You may use online references to understand the SSML specification, but DO NOT read
# online references for implementing an XML/SSML parser.
#


from dataclasses import dataclass
from typing import List, Union, Dict

SSMLNode = Union["SSMLText", "SSMLTag"]


@dataclass
class SSMLTag:
    name: str
    attributes: dict[str, str]
    children: list[SSMLNode]

    def __init__(
        self, name: str, attributes: Dict[str, str] = {}, children: List[SSMLNode] = []
    ):
        self.name = name
        self.attributes = attributes
        self.children = children


@dataclass
class SSMLText:
    text: str

    def __init__(self, text: str):
        self.text = text


def parseSSML(ssml: str) -> SSMLNode:

	# structure of SSMLNodeTree:
	# type key is either 'tag' or 'text'
	# code key is the entire code of ... hard to maintain,,.,
	# will adjust documentation as I make it.
	# complex whitespace not properly handled
	# no proper quotes matching '' or ""
	# kinda flaky... let's test
	# incomplete!


	#raise NotImplementedError()
	#result = 'hi from parseSSML'
	result = ''
	offset = node_offset = 0
	in_tag = False
	SSMLNodeTree = {}
	text = ''
	#parsing_text = True
	new_node = {'offset': offset, 'type': 'text', 'text': text}
	attributes = {}
	node_counter = 0
	debug_counter = 0
	while offset < len(ssml):
		#result += ssml[offset]
		#print('in first loop', ssml[offset])
		if ssml[offset] == '<':
			# add the last node, and start a new node
			new_node = {'offset': node_offset, 'type': 'text', 'text': text}
			SSMLNodeTree[node_counter] = new_node
			#parsing_text = False
			text = ''
			node_counter += 1
			new_node = {'offset': offset, 'type': 'tag'}
			attributes = {}
			in_tag = True
			in_tag_offset = offset + 1
			tagname = ''
			parsing_tagname = True
			parsed_tagname = False
			parsing_attribute_name = False
			parsing_attribute_value = False
			while ssml[in_tag_offset] != '>':
				#print('in second loop', ssml[in_tag_offset])
				if not parsed_tagname:
					if ssml[in_tag_offset] == ' ':
						new_node['tagname'] = tagname
						parsing_tagname = False
						parsed_tagname = True
				else:
					# parsing attributes
					if parsing_attribute_name:
						if ssml[in_tag_offset] == '=':
							parsing_attribute_name = False
							parsing_attribute_value = True
							in_tag_offset += 1 # skip the quote ' or "
						else:
							attribute_name += ssml[in_tag_offset]
					elif parsing_attribute_value:
						if ssml[in_tag_offset] == '"':
							parsing_attribute_name = True
							parsing_attribute_value = False
							attributes['name'] = attribute_name
							attributes['value'] = attribute_value
							attribute_name = ''
							attribute_value = ''
						else:
							attribute_value += ssml[in_tag_offset]
					else:
						print('ssml, in_tag_offset, SSMLNodeTree: ', ssml, in_tag_offset, SSMLNodeTree)
						print('should never get here0001')
						die()
				new_node['attributes'] = attributes
				in_tag_offset += 1
				debug_counter += 1
				if debug_counter > 20:
					print('debug break 1')
					break
			SSMLNodeTree[node_counter] = new_node
			in_tag = False
			text = ''
			offset = node_offset = in_tag_offset + 1
		if not in_tag:
			text += ssml[offset]
		offset += 1
		debug_counter += 1
		SSMLNodeTree[node_counter] = {'offset': node_offset, 'type': 'text', 'text': text}
		if debug_counter > 20:
			print('debug break 2')
			break
	return SSMLNodeTree


def ssmlNodeToText(node: SSMLNode) -> str:
    # TODO: implement this function
    raise NotImplementedError()


def unescapeXMLChars(text: str) -> str:
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def escapeXMLChars(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

# Example usage:
ssml_string = '<speak>Hello, <break time="500ms"/>world!</speak>'
parsed_ssml = parseSSML(ssml_string)
print(parsed_ssml)
