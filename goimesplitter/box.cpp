#include <Windows.h>
#include <iostream>
#include <string.h>

int main(){
	int i=0;
    for (HWND hwnd = GetTopWindow(NULL); hwnd != NULL; hwnd = GetNextWindow(hwnd, GW_HWNDNEXT))
    {   

	    if (!IsWindowVisible(hwnd))
	        continue;
	
	    int length = GetWindowTextLength(hwnd);
	    if (length == 0)
	        continue;
	
	    char* title = new char[length+1];
	    GetWindowText(hwnd, title, length+1);
	    
	    std::string str(title);
	
		if(str.find("Adobe Flash Player") != std::string::npos){
			RECT flp_size;
			bool a ;
			GetWindowRect(hwnd,&flp_size);
			
			std::cout << flp_size.left;
			std::cout << '\n';
			std::cout << flp_size.top;
			std::cout << '\n';
			std::cout << flp_size.bottom;
			std::cout << '\n';
			std::cout << flp_size.right;
			return 1;
			}
		}
    }

