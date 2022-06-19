#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

typedef struct node 
{
	unsigned long long ID;
	char buf[64];
	struct node *prev;
	struct node *next;
} node;

node *head,*tail;

void initialization()
{
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	alarm(30);
}

node *findnode(unsigned long long ID)
{
	node *curr = head;
	if(!head) return NULL;
	while(curr != NULL)
	{
		if(ID == curr->ID)
		{
			return curr;
		}
		curr = curr->next;
	}
	return NULL;
}

void insert()
{
	node *curr = (node *)calloc(1,sizeof(node));
	printf("ID: ");
	scanf("%llu",&curr->ID); getchar();
	printf("Content: ");
	read(0,curr->buf,63);
	if(!head || !tail) head = tail = curr;
	else
	{
		tail->next = curr;
		curr->prev = tail;
		tail = curr;
	}
}

void edit()
{
	node *curr;
	if(!head) printf("Empty\n");
	else
	{
		unsigned long long ID;
		printf("ID: ");
		scanf("%llu",&ID); getchar();
		if((curr = findnode(ID)) != NULL)
		{
			printf("New content: ");
			read(0,curr->buf,80);
		}
		else printf("Not found!\n");
	}
}

void view()
{
	node *curr;
	if(!head) printf("Empty\n");
	else
	{
		unsigned long long ID;
		printf("ID: ");
		scanf("%llu",&ID); getchar();
		if((curr = findnode(ID)) != NULL)
		{
			printf("Content: %s\n",curr->buf);
		}
		else printf("Not found!\n");
	}
}

void delete()
{
	node *curr;
	if(!head) printf("Empty\n");
	else
	{
		unsigned long long ID;
		printf("ID: ");
		scanf("%llu",&ID); getchar();
		if((curr = findnode(ID)) != NULL)
		{
			if(curr == head)
			{
				head = tail = NULL;
				free(curr);
			}
			else
			{
				curr->prev->next = curr->next;
				curr->next->prev = curr->prev;
				free(curr);
			}
		}
		else printf("Not found!\n");
	}
}

int main()
{
	char s[16];
	int choice,flag;
	flag = 0;
	initialization();
	do
	{
		printf("Linkedbin\n=========\n\n1. Insert\n2. Edit\n3. View\n4. Delete\n5. Exit\n\n");
		printf(">> ");
		fgets(s,16,stdin);
		choice = atoi(s);
		switch(choice)
		{
			case 1:
				insert();
				break;
			case 2:
				edit();
				break;
			case 3:
				view();
				break;
			case 4:
				delete();
				break;
			case 5:
				break;
			case 999:
				if(!flag && head != NULL)
				{
					node *curr = head;
					while(curr)
					{
						printf("ID: %llu\nContent: %s\n=================\n",curr->ID,curr->buf);
						curr = curr->next;
					}
					flag++;
				}
				break;
			default:
				printf("Invalid choice!\n");
				break;
		}
	}while(choice != 5);
	exit(0);
}