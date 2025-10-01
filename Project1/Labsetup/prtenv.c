#include <stdio.h>
void main()
{
	char * shell = getenv("MYSHELL");
	if(shell)
		printf("%x\n", (unsigned int)shell);
		printf("%s\n", shell);

	char * shell2 = getenv("ARG1");
	printf("%x\n", (unsigned int)shell2);
	printf("%s\n", shell2);

}
