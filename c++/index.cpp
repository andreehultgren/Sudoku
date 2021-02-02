
#include <iostream>
#include <string>
#include <cmath>
#include <conio.h>
#include <windows.h>

#define KEY_UP      72
#define KEY_DOWN    80
#define KEY_LEFT    75
#define KEY_RIGHT   77
#define ESC         27
#define ONE         49
#define TWO         50
#define THREE       51
#define FOUR        52
#define FIVE        53
#define SIX         54
#define SEVEN       55
#define EIGHT       56
#define NINE        57

using namespace std;

void set_cursor(int x = 0 , int y = 0)
{
    HANDLE handle;
    COORD coordinates;
    handle = GetStdHandle(STD_OUTPUT_HANDLE);
    coordinates.X = x;
    coordinates.Y = y;
    SetConsoleCursorPosition ( handle , coordinates );
}
void hidecursor()
{
   HANDLE consoleHandle = GetStdHandle(STD_OUTPUT_HANDLE);
   CONSOLE_CURSOR_INFO info;
   info.dwSize = 100;
   info.bVisible = FALSE;
   SetConsoleCursorInfo(consoleHandle, &info);
}

class Sudoku{
    public:
        bool solved;
        bool running;
        Sudoku(){
            // Set board as not solved
            solved = false;
            running= true;
            markerX = 0;
            markerY = 0;
            hidecursor();

            set_cursor(getX(markerX), getY(markerY));

            for(int x = 0; x < 9 ; x++){
                for(int y = 0; y < 9 ; y++){
                    board[x][y] = 0;
                }
            }
            drawBoard();
            generateBoard();
            
        }

        int getX(int x){
            return 4 + 6*x + floor(x/3);
        }
        int getY(int y){
            return 5 + 3*y + floor(y/3);
        }

        void generateBoard(){
            int nOnBoard = 0;
            while(nOnBoard<81){
                int x = round(rand()%9);
                int y = round(rand()%9);
                if(board[x][y] == 0){
                    int value = round(1+rand()%9);
                    board[x][y]=value;
                    if(isBoardValid()){
                        markerX = x;
                        markerY = y;
                        setValue(value);
                        nOnBoard++;
                    } else {
                        board[x][y]=0;
                    }
                }
            }
            markerX = 0;
            markerY = 0;
        }

        void drawBoard(){
            system("cls");
            cout << endl;
            cout <<  " ###################   SODUKO MASTER   ################### " << endl;
            cout <<  " _________________________________________________________ " << endl;
            cout <<  "|\\_______________________________________________________/|" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||     |     |     ||     |     |     ||     |     |     ||" << endl;
            cout <<  "||_____|_____|_____||_____|_____|_____||_____|_____|_____||" << endl;
            cout <<  "|/_______________________________________________________\\|" << endl;
        }

        void clearMarker(){
            set_cursor(getX(markerX)+2, getY(markerY)-1);
            cout << " ";
        }

        void setValue(int value){
            set_cursor(getX(markerX), getY(markerY));
            cout << value;
        }

        void checkIfSolved(){
            int nonZero = 0;
            for(int x = 0; x<9; x++){
                for(int y = 0; y<9; y++){
                    if(board[x][y] > 0){
                        nonZero++;
                    }
                }
            }
            if(nonZero==81 && isBoardValid()){
                set_cursor(1, 35);
                cout<< "You Solved the Sudoku!";
                solved=true;
            }
        }

        bool isBoardValid(){
            bool valid = true;
            int counts[10] = {0,0,0,0,0,0,0,0,0,0};
            // Check x-directions
            for(int y = 0 ; y < 9 ; y++){
                // Count the row
                for(int x = 0 ; x < 9 ; x++)    counts[board[x][y]]++;
                
                // Invalidate board if non-zero count is larger than one
                for(int n = 1; n<=9 ; n++)      if(counts[n] > 1) valid=false;

                // Reset counts
                for(int n=0;n<=9;n++)           counts[n]=0;
                
            }

            // Check y-directions
            for(int x = 0 ; x < 9 ; x++){
                // Count the row
                for(int y = 0 ; y < 9 ; y++)    counts[board[x][y]]++;
                
                // Invalidate board if non-zero count is larger than one
                for(int n = 1; n <= 9 ; n++)    if(counts[n] > 1) valid=false;

                // Reset counts
                for(int n = 0 ; n <= 9 ; n++)   counts[n]=0;
            }

            // Check each square
            for(int i = 0; i< 3 ; i++){
                for(int j = 0; j < 3 ; j++){
                    // Check the 9 elements of the square
                    for(int x = 0 ; x<3; x++){
                        for(int y = 0 ; y<3; y++){
                            int xPos = i*3+x;
                            int yPos = j*3+y;
                            counts[board[xPos][yPos]]++;
                        }
                    }
                    // Invalidate board if non-zero count is larger than one
                    for(int n = 1; n <= 9 ; n++)    if(counts[n] > 1) valid=false;

                    // Reset counts
                    for(int n = 0 ; n <= 9 ; n++)   counts[n]=0;
                }
            }
            return valid;
        }

        void listen(){
            // Clear marker
            set_cursor(getX(markerX)+2, getY(markerY)-1);
            cout << "*";
            set_cursor(0, 0);

            int c = 0;

            switch((c=getch())) {
                case KEY_UP:
                    clearMarker();
                    markerY--;
                    break;
                case KEY_DOWN:
                    clearMarker();
                    markerY++;
                    break;
                case KEY_LEFT:
                    clearMarker();
                    markerX--;
                    break;
                case KEY_RIGHT:
                    clearMarker();
                    markerX++;
                    break;
                case ESC:
                    running=false;
                default:
                    int input = (int)c - 48;
                    if(input >0 && input < 10){
                        board[markerX][markerY] = input;
                        setValue(input);
                    }
                    break;
            }
            if(markerX < 0)     markerX = 0;
            if(markerX > 8)     markerX = 8;
            if(markerY < 0)     markerY = 0;
            if(markerY > 8)     markerY = 8;
            
            checkIfSolved();
            
            if(!isBoardValid()){
                set_cursor(1, 35);
                cout<< "Board Not Valid";
            } else {
                set_cursor(1, 35);
                cout<< "               ";
            }
        }

    private:
        int markerX;
        int markerY;
        int board[9][9];
};

int main(){
    Sudoku board;
    
    while(board.running && !board.solved){
        board.listen();
    }

    if(board.solved){
        cout << "YOU SOLVED IT! WAY TO GO!!";
    }

    return 0;
}