#!/usr/bin/env python

from xml.dom import minidom
from pydoc import doc

"""
Create and edit a directory like xml file
"""
class XmlDirectory():
    
    def __init__(self):
        
        # Create document
        self.doc = minidom.Document()
        self.root = self.doc.createElement('document')
        rootattr = self.doc.createAttribute('type')
        rootattr.nodeValue = 'Freeswitch/xml'
        self.root.setAttributeNode(rootattr)
        self.doc.appendChild(self.root)
        
        #Add a new section to the document
        section = self.doc.createElement('section')
        sectionAttr = self.doc.createAttribute('name')
        sectionAttr.nodeValue = 'directory'
        section.setAttributeNode(sectionAttr)
        self.root.appendChild(section)


    def getXmlDoc(self):
        return self.doc
    
    def getDocRoot(self):
        return self.root

    
    """
    Add a new domain to the section
    """
    def addNewDomain(self, dn):
        
        exists = False
        
        for element in self.doc.getElementsByTagName('domain'):
            if element.getAttribute('name') == dn:
                exists = True
        
        if exists == False:
            print exists
            params = self.doc.createElement('params')
            variables = self.doc.createElement('variables')
        
            domain = self.doc.createElement('domain')
            domainattr = self.doc.createAttribute('name')
            domainattr.nodeValue = dn
            domain.setAttributeNode(domainattr)
        
            domain.appendChild(params)
            domain.appendChild(variables)
        
            section = self.doc.getElementsByTagName('section')
            section[0].appendChild(domain)
        else:
            print('domain exists')
            exit(0)


    """
    Set doc parameters
    """
    def addParameter(self, dn, **kwargs):
        doc = self.doc
        
        param = self.doc.createElement('param')
        
        for key, value in kwargs.iteritems():
            paramattr = self.doc.createAttribute(key)
            paramattr.nodeValue = value
            param.setAttributeNode(paramattr)
        
        # Search all domains
        for element in doc.getElementsByTagName('domain'):
            #Search for a domain matching the one needed
            if element.getAttribute('name') == dn:
                # Domain exists: add parameter
                param_list = self.doc.getElementsByTagName('params')
                param_list[0].appendChild(param)
            else:
                # domain does not exists: create it and add parameter
                self.addNewDomain(dn)
                self.addParameter(dn, kwargs)
    
    
    """
    Add user node 
    """
    def addUser(self, dn, username, password, gn=None):
        doc = self.doc
        
        
        for element in doc.getElementsByTagName('domain'):
            if element.getAttribute('name') == dn:
                
                user_list = doc.createElement('users')
                user = doc.createElement('user')
                
                user_params = doc.createElement('params')
                user_param = doc.createElement('param')
                user_param_nameattr = doc.createAttribute('name')
                user_param_nameattr.nodeValue = username
                user_param_hashattr = doc.createAttribute('password')
                user_param_hashattr.nodeValue = password
                
                user_param.setAttributeNode(user_param_nameattr)
                user_param.setAttributeNode(user_param_hashattr)
                
                user_params.appendChild(user_param)
                user.appendChild(user_params)
                user_list.appendChild(user)
                
                
                if gn is not None:
                    group_list = doc.createElement('groups')
                    group = doc.createElement('group')
                    groupattr = doc.createAttribute('name')
                    groupattr.nodeValue = gn
                    group.setAttributeNode(groupattr)
                    
                    group.appendChild(user_list)
                    group_list.appendChild(group)
                    element.appendChild(group_list)
                else:
                    element.appendChild(user_list)
            else:
                print('Invalid domain')
                    
       
if __name__ == '__main__':
    
    newdoc = XmlDirectory()
    root = newdoc.getDocRoot()
    doc = newdoc.getXmlDoc()
    newdoc.addNewDomain('sip.freeswitch.com')
    newdoc.addParameter('sip.freeswitch.com', name='dial-string', value='{presence_id=${dialed_user}@${dialed_domain}}${sofia_contact(${dialed_user}@${dialed_domain})}')
    newdoc.addUser('sip.freeswitch.com', '1001', 'abcd', 'default')
    
    print doc.toprettyxml()