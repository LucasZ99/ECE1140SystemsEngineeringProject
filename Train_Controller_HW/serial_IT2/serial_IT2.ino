int incomingByte = 0; // for incoming serial data
String TrainModel_arr[12];
int Driver_arr[11];
int StringCount = 0;


int TCK_Kp  = 0;
int TCK_Ki      = 1;
int TCK_CmdSpd  = 2;
int TCK_Temp    = 3;
//digital
/*
LED_CabnLgt    = 
LED_HeadLgt    = 
LED_Door_L     = 
LED_Door_R     = 
LED_Pass_EB    = 
LED_Track_Circ = 
LED_Stat_Side2 = 
LED_Stat_Side1 = 
LED_Sig_Fail   = 
LED_Eng_Fail   = 
LED_Brk_Fail   = 
*/

int BTN_CabnLgt = 40;
int BTN_HeadLgt = 41;
int BTN_Door_L  = 42;
int BTN_Door_R  = 43;
int BTN_EBRK    = 44;
int BTN_SBRK    = 45;
int BTN_DisPaEB = 46;

/*
int BTN_CabnLgt = 4;
int BTN_HeadLgt = 5;
int BTN_Door_L  = 6;
int BTN_Door_R  = 7;
int BTN_EBRK    = 8;
int BTN_SBRK    = 9;
int BTN_DisPaEB = 10;
*/
void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps

  pinMode(BTN_CabnLgt, INPUT);
  pinMode(BTN_HeadLgt, INPUT);   
  pinMode(BTN_Door_L, INPUT);
  pinMode(BTN_Door_R, INPUT);   
  pinMode(BTN_EBRK, INPUT);
  pinMode(BTN_SBRK, INPUT);   
  pinMode(BTN_DisPaEB, INPUT);
}

void loop() {
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    String incomingString = Serial.readString();

    // prints the received data
    //Serial.print("I received: ");
    //Serial.println(incomingString);

    while (incomingString.length() > 0)
  {
    int index = incomingString.indexOf(", ");
    if (index == -1) // No space found
    {
      TrainModel_arr[StringCount++] = incomingString;
      break;
    }
    else
    {
      TrainModel_arr[StringCount++] = incomingString.substring(0, index);
      incomingString = incomingString.substring(index+1);
    }
  }
  /*
  for (int i = 0; i < StringCount; i++)
  {
    Serial.print(i);
    Serial.print(": ");
    Serial.println(TrainModel_arr[i]);
  }*/
  }
  
  //prepare return array
  Driver_arr[0] = analogRead(TCK_Kp);
  Driver_arr[1] = analogRead(TCK_Ki);
  Driver_arr[2] = analogRead(TCK_CmdSpd);
  Driver_arr[5] = analogRead(TCK_Temp);
  
  if(digitalRead(BTN_CabnLgt) == LOW ){Driver_arr[3] = 0;}
  else{Driver_arr[3] = 1;}
  if(digitalRead(BTN_HeadLgt) == LOW ){Driver_arr[4] = 0;}
  else{Driver_arr[4] = 1;}
  if(digitalRead(BTN_Door_L) == LOW ){Driver_arr[6] = 0;}
  else{Driver_arr[6] = 1;}
  if(digitalRead(BTN_Door_R) == LOW ){Driver_arr[7] = 0;}
  else{Driver_arr[7] = 1;}
  if(digitalRead(BTN_EBRK) == LOW ){Driver_arr[8] = 0;}
  else{Driver_arr[8] = 1;}
  if(digitalRead(BTN_SBRK) == LOW ){Driver_arr[9] = 0;}
  else{Driver_arr[9] = 1;}
  if(digitalRead(BTN_DisPaEB) == LOW ){Driver_arr[10] = 0;}
  else{Driver_arr[10] = 1;}
  for (int i = 0; i < 12; i++)
  {
    Serial.print(Driver_arr[i]);
    Serial.print(", ");
  }
  Serial.println("");

  //set leds




}
