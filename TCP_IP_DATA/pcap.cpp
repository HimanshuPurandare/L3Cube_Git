#include <stdio.h>
#include <pcap.h>
#include <stdlib.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <string.h>
#include <iostream>
using namespace std;

#define ETHER_TYPE_IP (0x0800)
#define ETHER_TYPE_ARP (0x0806)

class PcapReader
{
	/*Header of a packet in the dump file.Each packet in the dump file is prepended with this generic header. This gets around the problem of different headers for different packet interfaces.*/
	struct pcap_pkthdr header;          
	
	/*handle to the file to be analysed*/
	pcap_t *handle;   
	
	/*buffer to store the error message*/
    char errbuf[PCAP_ERRBUF_SIZE];      
    
    public:
    
    /*The following function returns a handle to the file to be analysed*/
    pcap_t* open_file(char* filename)
    {
        this->handle = pcap_open_offline(filename, errbuf); 
    	return (this->handle);
    }
    
    /*The following function analyses the pcap file*/
    void analyse_file(pcap_t* handle)
    {
    	this->handle = handle;
    	const u_char *packet;
		int packet_count = 0;
		
		/*The loop will analyse all the packets present in the pcap file*/
	    while ((packet = pcap_next(this->handle,&(this->header))) ) 
	    {	
	    	packet_count++;
	    	printf("Packet %d\n",packet_count);
			u_char *pkt_ptr = (u_char *)packet;
    		analyse_packet(pkt_ptr);
    		printf("-----------------------------------------------------\n");
    	}
    }
    
    /*The following function reads single packet in the file*/
    void analyse_packet(u_char* pkt_ptr)
    {
    	printf("  Ethernet Header\n");
    	print_dest_mac_addr(pkt_ptr);
    	print_source_mac_addr(pkt_ptr);
    	int ether_type = get_eth_type(pkt_ptr);
    	
    	/*Check whether it is an IP packet*/
    	if(ether_type == ETHER_TYPE_IP)
    	{
    		/*Add the Ethernet frame header length to the pointer*/
			pkt_ptr += 14;
			printf("  IP header\n");
			
			/*Print the IP header details and get the protocol(at transport layer) number*/
			int protocol_number = analyse_ip_header(pkt_ptr);   
			 	
			/*Check whether it uses TCP*/
			if(protocol_number == 6) 
			{
				analyse_tcp_header(pkt_ptr);
			}
						
			/*If not, check for UDP*/
			else if(protocol_number == 17)
			{
				printf("  UDP packet");
			}
			
			else
			{
				printf("Other packet type\n");
			}
    	}
    	
    	/*If not, check for ARP*/
    	else if(ether_type == ETHER_TYPE_ARP)
		{
			pkt_ptr += 14;
			analyse_arp_header(pkt_ptr);
		}
		
		/*If not any of the above...*/
		else
		{
				printf("Other packet type\n");
		}
    }
    
    /*Prints the destination MAC address from the ethernet frame header*/
    void print_dest_mac_addr(u_char* pkt_ptr)
    {
    	printf("	Destination Mac address --> ");
    	for(int k=0;k<=5;k++)
    	{
			printf("%x",((int)(pkt_ptr[k])));
			if(k==5)
				break;
			printf(":");
				
		}	
		printf("\n");
    }
    
    /*Prints the source MAC address from the ethernet frame header*/
    void print_source_mac_addr(u_char* pkt_ptr)
    {
    	printf("	Source Mac address --> ");
    	for(int k=6;k<=11;k++)
    	{
			printf("%x",((int)(pkt_ptr[k])));
			if(k==11)
				break;
			printf(":");
		}	
		printf("\b \n");
    }    
    
    /*Get the ethernet payload type*/
    int get_eth_type(u_char* pkt_ptr)
    {
    	int ether_type = ((int)(pkt_ptr[12]) << 8) | (int)pkt_ptr[13];
    	return ether_type;
    }
    
    /*Prints the details of the IP payload contained by the ethernet frame*/
    int analyse_ip_header(u_char* pkt_ptr)
    {
    	printf("	IP Version : %d\n",((*pkt_ptr) >> 4));
 		int ip_header_length = 4*((*pkt_ptr) & (0x0f));
 		printf("	IP header length : %d\n",ip_header_length);
 		pkt_ptr+=1;
 		printf("	Type of Service : 0x%x\n",(*pkt_ptr));
 		pkt_ptr+=1;
 		printf("	Total length : %d\n",(((*pkt_ptr) << 8) | (*(pkt_ptr+1))));
 		pkt_ptr+=2;
 		printf("	Identification : %d\n",(((*pkt_ptr) << 8) | (*(pkt_ptr+1))));
 		pkt_ptr+=2;
 		printf("	Flags : \n");
 		printf("			MF = %d\n",((*pkt_ptr) & (0x20)));
 		printf("        	DF = %d\n",((*pkt_ptr) & (0x40)));
 		printf("        	RES = %d\n",((*pkt_ptr) & (0x80)));
 		printf("	Fragment offset : 0x%x\n",(((*pkt_ptr) & (0x1f)) << 8) | (*(pkt_ptr+1)));
 		pkt_ptr+=2;
 		printf("	TTL : %d\n",(*pkt_ptr));
 		pkt_ptr+=1;
 		int protocol_number = (*pkt_ptr);
 		printf("	Protocol : %d",protocol_number);
 		switch(protocol_number)
 		{
 			case 1:
 				printf("(ICMP)\n");
 				break;
 			case 2:
 				printf("(IGMP)\n");
 				break;
 			case 6:
 				printf("(TCP)\n");
 				break; 	
 			case 17:
 				printf("(UDP)\n");
 				break; 
 			default:
 				break; 											
 		}
 		pkt_ptr+=1;
 		printf("	Header Checksum : 0x%x\n",(((*pkt_ptr) << 8) | (*(pkt_ptr+1))));
 		pkt_ptr+=2;
 		printf("	Source IP : ");
 		for(int j=0;j<4;j++)
 		{
 			printf("%d",(*(pkt_ptr+j)));
 			if(j==3)
 			 	break;
 			printf(".");
 		}
 		printf("\n");
 		pkt_ptr+=4;
 		printf("	Destination IP : ");
 		for(int j=0;j<4;j++)
 		{
 			printf("%d",(*(pkt_ptr+j)));
 			if(j==3)
 			 	break;
 			printf("."); 			
 		}
 		printf("\n");
 		pkt_ptr += 4;
 		return protocol_number;
    }
    
    /*Prints the details of the TCP payload contained by the IP packet */
    void analyse_tcp_header(u_char* pkt_ptr)
    {
    	int ip_header_length = 4*((*pkt_ptr) & (0x0f));
    	pkt_ptr = pkt_ptr + ip_header_length;

		printf("  TCP header\n");
		int srcp = ((int)(*pkt_ptr) << 8) | (int)(*(pkt_ptr+1));
		printf("	Source port: %d",srcp - 80);
		if(srcp == 179 )
		{
			printf(" (BGP)");
		}
		else if(srcp == 80 )
		{
			printf(" (HTTP)");
		}
		printf("\n");
		pkt_ptr+=2;
		int dstp = ((int)(*pkt_ptr) << 8) | (int)(*(pkt_ptr+1));
		printf("	Destination port: %d",dstp);
		pkt_ptr+=2;
		if(dstp == 80)
		{
			printf(" (HTTP)");
		}
		else if(dstp == 179 )
		{
			printf(" (BGP)");
		}
		printf("\n");
		printf("	Sequence number :- 0x%x\n",((int)(*pkt_ptr) << 24) | (((int)(*(pkt_ptr+1)) << 16) ) | (((int)(*(pkt_ptr+2)) << 8) ) |(((int)(*(pkt_ptr+3))) ));
		pkt_ptr+=4;
		
		printf("	Acknowledgement number :- 0x%x\n",((int)(*pkt_ptr) << 24) | (((int)(*(pkt_ptr+1)) << 16) ) | (((int)(*(pkt_ptr+2)) << 8) ) |(((int)(*(pkt_ptr+3))) ));
		pkt_ptr+=4;
		int dof = (*pkt_ptr)/(0x10)*4;
		printf("	Data offset: %d bytes\n",(*pkt_ptr)/(0x10)*4);
		printf("	Control bits : \n");
		printf("		Nonce : %d\n",dof & 1);
		pkt_ptr+=1;
		dof = *pkt_ptr;
		int bit = 256;
		printf("		CWR : %d\n",dof & bit?1:0 );
		bit = bit >> 1;
		printf("		ECE : %d\n",dof & bit?1:0);
		bit = bit >> 1;
		printf("		URG : %d\n",dof & bit?1:0);
		bit = bit >> 1;
		printf("		ACK : %d\n",dof & bit?1:0);
		bit = bit >> 1;
		printf("		PSH : %d\n",dof & bit?1:0);
		bit = bit >> 1;
		printf("		RST : %d\n",dof & bit?1:0);
		bit = bit >> 1;
		printf("		SYN : %d\n",dof & bit?1:0);
		bit = bit >> 1;
		printf("		FIN : %d\n",dof & bit?1:0);
		
		pkt_ptr+=1;
		
		printf("	Window size : %d\n",((int)(*pkt_ptr) << 8) | (int)(*(pkt_ptr+1)));
		pkt_ptr+=2;
		printf("	Checksum : 0x%x\n",((int)(*pkt_ptr) << 8) | (int)(*(pkt_ptr+1)));
		pkt_ptr+=2;
		printf("	Urgent Pointer : %d\n",((int)(*pkt_ptr) << 8) | (int)(*(pkt_ptr+1)));
		
		if(srcp==80 || dstp==80)
		{
			analyse_http_header(srcp,dstp,pkt_ptr);
		}
    }
    
    /*Prints the details of the ARP payload contained by the ethernet frame*/  
    void analyse_arp_header(u_char* pkt_ptr)
    {
    	int k=0;
		printf("  ARP header\n");
		printf("	Hardware type : 0x%x\n",((*pkt_ptr)<<8) | (*pkt_ptr+1));
		pkt_ptr+=2;
		printf("	Protocol type : 0x%x\n",((*pkt_ptr)<<8) | (*(pkt_ptr+1)));
		pkt_ptr+=2;
		printf("	Hardware length : %d\n",(*pkt_ptr));
		pkt_ptr+=1;
		printf("	Protocol length : %d\n",(*pkt_ptr));
		pkt_ptr+=1;
		int op_code=((*pkt_ptr)<<8) | (*pkt_ptr+1);
		printf("	Operation Code : %d",op_code);
		switch(op_code)
		{
			case 1:
				printf("(ARP REQUEST)");
				break;
			case 2:
				printf("(ARP RESPONSE)");
				break;
			default:
				break;
		}
		printf("\n");
		pkt_ptr+=2;
		printf("	Sender Hardware Address : ");
		for(k=0;k<6;k++)
		{
			printf("%x",(*(pkt_ptr+k)));
			if(k==5)
				break;
				
			printf(":");
		}
		printf("\n");
		pkt_ptr+=6;
		printf("	Sender Protocol Address : ");
		for(k=0;k<4;k++)
		{
			printf("%d",(*(pkt_ptr+k)));
			if(k==3)
				break;
				
			printf(".");
		}
		printf("\n");
		pkt_ptr+=4;
		printf("	Target Hardware Address : ");
		for(k=0;k<6;k++)
		{
			printf("%x",(*(pkt_ptr+k)));
			if(k==5)
				break;
				
			printf(":");
		}
		printf("\n");
		pkt_ptr+=6;
		printf("	Target Protocol Address : ");
		for(k=0;k<4;k++)
		{
			printf("%d",(*(pkt_ptr+k)));
			if(k==3)
				break;
				
			printf(".");
		}
		printf("\n");
    }
    
    void analyse_http_header(int srcp, int dstp,u_char* pkt_ptr)
    {
    	int k=0;
    	char v;
    	printf("  HTTP Header \n");
    	if(dstp == 80)
		{
			printf("	Request packet\n");		
		}
		else
		{
			printf("	Response packet\n");
		}
    }
};


int main(int argc, char **argv)
{
	/*Check the number of command line arguments*/
	if (argc < 2) 
	{ 
		fprintf(stderr, "Usage: %s [input pcaps]\n", argv[0]); 
		exit(1); 
	}
	
	/*Create a reader*/
	PcapReader p;
	
	/*Analyse every file specified in the command line*/
	for(int i=1;i<argc;i++)
	{
		pcap_t* handle = p.open_file(argv[i]);
	
		if (handle == NULL) 
		{ 
			printf("Unable to open file");
 	   	 	return(2); 
    	}
    
 	   p.analyse_file(handle);	
	}	
	return 0;
}
