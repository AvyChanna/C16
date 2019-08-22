#include<iostream>
#include<fstream>
#include<vector>
#include<string>
using namespace std;

int main(int argc, char ** argv){
	if(argc !=2)
	{
		cout<<"Provide exactly 1 arg"<<endl;
		return 0;
	}
	vector<string> fname;
	vector<string> fname2;
	ifstream fin(argv[1]);
	vector<string> line;
	int i, j;
	char sum;
	char nb;
	short iaddr;
	vector<string> values;
	char * fnamep;
	fstream fout, fout2;

	fnamep = 

}