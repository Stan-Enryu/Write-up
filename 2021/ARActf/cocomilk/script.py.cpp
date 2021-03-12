#include <iostream>
#include <string>
#include <bits/stdc++.h> 
using namespace std;
string z(string a);string y(string b);
int main() {string a;cout<<"Input: ";cin>>a;

a = input("Input: ")
b = ""
c = ""
cout << z(a) << endl;
return 0;
}

string z(string a) {string b = "";
for (int i = 0; i < a.length(); i+=2) {
	b += a[i];
	
}return y(b);}

string y(string b) {
string a = "";
for (int i = 0;i < b.length(); i++) {
a+=b[i]^i;
}
reverse(a.begin(), a.end());
return a;
}

