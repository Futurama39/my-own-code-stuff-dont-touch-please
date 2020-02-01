#include <bits/stdc++.h>
#include <stdio.h> 
#include <math.h>
using namespace std; 
  
void SieveOfEratosthenes(long long int n) 
{ 

    bool prime[n+1]; 
    memset(prime, true, sizeof(prime)); 
  
    for (long long int p=2; p*p<=n; p++) 
    { 

        if (prime[p] == true) 
        { 

            for (long long int i=p*p; i<=n; i += p) 
                prime[i] = false; 
        } 
    } 
  

	for (long long int p=2; p<=n; p++) 
   		if (prime[p]) 
        cout << p << " "; 
} 
  

int main() 
{ 
    long long int n = pow(10,9); 
    cout << "Following are the prime numbers smaller "
         << " than or equal to " << n << endl; 
    SieveOfEratosthenes(n); 
    return 0; 
} 
