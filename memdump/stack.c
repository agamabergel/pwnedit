#include <stdio.h>
#include <stdlib.h>



int main()
{
	char* str1 = "HOLY SHIT WERE ON THE STACK";
	char* str2 = "stack twice :)))))";
	char* mm1 = (char*)malloc(sizeof(char) * 24);
	*mm1 = "omg the heappppp";
	
	sleep(1000000000000);
	return 0;
}

