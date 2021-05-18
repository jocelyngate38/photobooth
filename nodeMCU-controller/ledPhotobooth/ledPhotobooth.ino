#include <Adafruit_NeoPixel.h>
#include <CmdMessenger.h>

#define PHOTOBOOTH_2

#ifdef PHOTOBOOTH_1
int approchez[2] = {0, 19};
int appareilphoto[2] = {19, 41};
int boxaselfi[2] = {41, 59};
int sideRight[2] = {59, 79};
int frontRight[2] = {79, 89};
int frontLeft[2] = {89, 99};
int sideLeft[2] = {99, 119};
#endif

#ifdef PHOTOBOOTH_2
int approchez[2] = {0, 20};
int appareilphoto[2] = {20, 40};
int boxaselfi[2] = {40, 60};
int sideRight[2] = {60, 80};
int frontRight[2] = {80, 89};
int frontLeft[2] = {89, 100};
int sideLeft[2] = {100, 119};
#endif


const uint16_t PixelCount = sideLeft[1];
uint8_t brightness = 200;

struct {

  int r = 0;//255;
  int g = 0;
  int b = 0;

} LEDS_CAMERA_BACK_COLOR;

struct {

  int r = 0;
  int g = 0;
  int b = 0;//255;

} LEDS_TEXT_BACK_COLOR;

struct {

  int r = 0;
  int g = 0;
  int b = 0;//255;

} LEDS_SIDE_LEFT_COLOR;

struct {

  int r = 0;
  int g = 0;
  int b = 0;//255;

} LEDS_SIDE_RIGHT_COLOR;

struct {

  int r = 0;//255;
  int g = 0;//255;
  int b = 0;//255;

} LEDS_FRONT_COLOR_1;

struct {

  int r = 0;
  int g = 0;
  int b = 0;//255;

} LEDS_FRONT_COLOR_2;

struct {

  int r = 0;//255;
  int g = 0;
  int b = 0;

} LEDS_ERROR_COLOR_1;

struct {

  int r = 0;
  int g = 0;
  int b = 0;

} LEDS_ERROR_COLOR_2;

struct {

  long timerMS  = 0;
  long timeoutMs = 4000;
  long blinkingDelayMs = 300;
  long blinkingTimerMs = 0;
  bool blinking = 0;
  int index = 0;
  bool updateRequest = true;
  bool updated = false;

} LEDS_FRONT;

struct {

  long timerMS  = 0;
  long timeoutMs = 4000;
  long blinkingDelayMs = 300;
  long blinkingTimerMs = 0;
  bool blinking = 0;
  int index = 0;
  bool updateRequest = true;
  bool updated = false;

} LEDS_SIDE_RIGHT;

struct {

  long timerMS  = 0;
  long timeoutMs = 4000;
  long blinkingDelayMs = 300;
  long blinkingTimerMs = 0;
  bool blinking = 0;
  int index = 0;
  bool updateRequest = true;
  bool updated = false;

} LEDS_SIDE_LEFT;

struct {

  long timerMS  = 0;
  long timeoutMs = 4000;
  long blinkingDelayMs = 300;
  long blinkingTimerMs = 0;
  bool blinking = 0;
  int index = 0;
  bool updateRequest = true;
  bool updated = false;

} LEDS_CAMERA_BACK;

struct {

  long timerMS  = 0;
  long timeoutMs = 4000;
  long blinkingDelayMs = 300;
  long blinkingTimerMs = 0;
  bool blinking = 0;
  int index = 0;
  bool updateRequest = true;
  bool updated = false;

} LEDS_TEXT_BACK;


struct {

  long timerMS  = 0;
  long timeoutMs = 4000;
  long blinkingDelayMs = 500;
  long blinkingTimerMs = 0;
  bool blinking = 0;
  int index = 0;
  bool updateRequest = false;
  bool updated = false;

} LEDS_ERROR_STATE;


enum {

  kAcknowledge,
  kError,
  kCommandList,
  kReset,
  kBlinkFront,
  kSetFrontColor,
  kSetSideRightColor,
  kSetSideLeftColor,
  kSetBackTextColor,
  kSetBackCameraColor,
  kSetPrinterError,
  kSetErrorColor,
  kSetBrightness,

};

Adafruit_NeoPixel strip = Adafruit_NeoPixel(PixelCount, D4, NEO_GRB + NEO_KHZ800);
CmdMessenger cmdMessenger = CmdMessenger(Serial);


void attachCommandCallbacks()
{
  // Attach callback methods
  cmdMessenger.attach(onUnknownCommand);
  cmdMessenger.attach(kCommandList, onCommandList);
  cmdMessenger.attach(kReset, onReset);
  cmdMessenger.attach(kBlinkFront, onBlinkFront);
  cmdMessenger.attach(kSetFrontColor, onSetFrontColor);
  cmdMessenger.attach(kSetSideRightColor, onSetSideRightColor);
  cmdMessenger.attach(kSetSideLeftColor, onSetSideLeftColor);
  cmdMessenger.attach(kSetBackTextColor, onSetBackTextColor);
  cmdMessenger.attach(kSetBackCameraColor, onSetBackCameraColor);
  cmdMessenger.attach(kSetPrinterError, onSetPrinterError);
  cmdMessenger.attach(kSetErrorColor, onSetErrorColor);
  cmdMessenger.attach(kSetBrightness, onSetBrightness);


}




void onUnknownCommand() {

  Serial.println("Unknown command");
  cmdMessenger.sendCmd(kError, "onUnknownCommand triggered!");

}

void onReset() {

  Serial.println("onReset command");
  cmdMessenger.sendCmd(kAcknowledge, "onReset triggered!");
  ESP.restart();

}

void onCommandList() {

  LEDS_FRONT.updateRequest = true;
  LEDS_FRONT.updated = false;

  Serial.println("List of rdesponses");
  Serial.print("kAcknowledge: ");         Serial.print(kAcknowledge);         Serial.println(" when command succeed.");
  Serial.print("kError: ");               Serial.print(kError);               Serial.println(" if command errors.");
  Serial.println("List of commands");
  Serial.print("kCommandList: ");         Serial.print(kCommandList);         Serial.println(";");
  Serial.print("kReset: ");               Serial.print(kReset);               Serial.println(";");
  Serial.print("kBlinkFront: ");          Serial.print(kBlinkFront);          Serial.println(",<blink[default 200ms]>;");
  Serial.print("kSetFrontColor: ");       Serial.print(kSetFrontColor);       Serial.println(",<red_1>,<green_1>,<blue_1>,<red_2>,<green_2>,<blue_2>; uint8_t [0,255]");
  Serial.print("kSetSideRightColor: ");   Serial.print(kSetSideRightColor);   Serial.println(",<red>,<green>,<blue>; uint8_t [0,255]");
  Serial.print("kSetSideLeftColor: ");    Serial.print(kSetSideLeftColor);    Serial.println(",<red>,<green>,<blue>; uint8_t [0,255]");
  Serial.print("kSetBackTextColor: ");    Serial.print(kSetBackTextColor);    Serial.println(",<red>,<green>,<blue>; uint8_t [0,255]");
  Serial.print("kSetBackCameraColor: ");  Serial.print(kSetBackCameraColor);  Serial.println(",<red>,<green>,<blue>; uint8_t [0,255]");
  Serial.print("kSetPrinterError: ");     Serial.print(kSetPrinterError);     Serial.println(",<bool>; [0=no error or 1=error state]");
  Serial.print("kSetErrorColor: ");       Serial.print(kSetErrorColor);       Serial.println(",<red_1>,<green_1>,<blue_1>,<red_2>,<green_2>,<blue_2>; uint8_t [0,255]");
  Serial.print("kSetBrightness: ");       Serial.print(kSetBrightness);       Serial.println(",<brightness>; uint8_t [0,255]");

  cmdMessenger.sendCmd(kAcknowledge, "onCommandList triggered!");
}

void onBlinkFront() {

  LEDS_FRONT.blinkingDelayMs = cmdMessenger.readInt16Arg();
  LEDS_FRONT.updateRequest = true;
  LEDS_FRONT.updated = false;
  LEDS_FRONT.blinking = true;
  LEDS_FRONT.index = 0;
  LEDS_FRONT.timerMS = millis() + LEDS_FRONT.timeoutMs;
  cmdMessenger.sendCmd(kAcknowledge, "onBlinkFront triggered!");
}

void onSetFrontColor() {

  LEDS_FRONT_COLOR_1.r = cmdMessenger.readInt16Arg();
  LEDS_FRONT_COLOR_1.g = cmdMessenger.readInt16Arg();
  LEDS_FRONT_COLOR_1.b = cmdMessenger.readInt16Arg();

  LEDS_FRONT_COLOR_2.r = cmdMessenger.readInt16Arg();
  LEDS_FRONT_COLOR_2.g = cmdMessenger.readInt16Arg();
  LEDS_FRONT_COLOR_2.b = cmdMessenger.readInt16Arg();

  LEDS_FRONT.updateRequest = true;
  LEDS_FRONT.updated = false;

  cmdMessenger.sendCmd(kAcknowledge, "onSetFrontColor triggered!");
}

void onSetErrorColor() {

  LEDS_ERROR_COLOR_1.r = cmdMessenger.readInt16Arg();
  LEDS_ERROR_COLOR_1.g = cmdMessenger.readInt16Arg();
  LEDS_ERROR_COLOR_1.b = cmdMessenger.readInt16Arg();

  LEDS_ERROR_COLOR_2.r = cmdMessenger.readInt16Arg();
  LEDS_ERROR_COLOR_2.g = cmdMessenger.readInt16Arg();
  LEDS_ERROR_COLOR_2.b = cmdMessenger.readInt16Arg();

  LEDS_FRONT.updateRequest = true;
  LEDS_FRONT.updated = false;

  cmdMessenger.sendCmd(kAcknowledge, "onSetFrontColor triggered!");

}

void onSetSideRightColor() {

  LEDS_SIDE_RIGHT_COLOR.r = cmdMessenger.readInt16Arg();
  LEDS_SIDE_RIGHT_COLOR.g = cmdMessenger.readInt16Arg();
  LEDS_SIDE_RIGHT_COLOR.b = cmdMessenger.readInt16Arg();

  LEDS_SIDE_RIGHT.updateRequest = true;
  LEDS_SIDE_RIGHT.updated = false;

  cmdMessenger.sendCmd(kAcknowledge, "onSetSideRightColor triggered!");
}

void onSetSideLeftColor() {

  LEDS_SIDE_LEFT_COLOR.r = cmdMessenger.readInt16Arg();
  LEDS_SIDE_LEFT_COLOR.g = cmdMessenger.readInt16Arg();
  LEDS_SIDE_LEFT_COLOR.b = cmdMessenger.readInt16Arg();

  LEDS_SIDE_LEFT.updateRequest = true;
  LEDS_SIDE_LEFT.updated = false;

  cmdMessenger.sendCmd(kAcknowledge, "onSetSideLeftColor triggered!");
}

void onSetBackTextColor() {

  LEDS_TEXT_BACK_COLOR.r = cmdMessenger.readInt16Arg();
  LEDS_TEXT_BACK_COLOR.g = cmdMessenger.readInt16Arg();
  LEDS_TEXT_BACK_COLOR.b = cmdMessenger.readInt16Arg();

  LEDS_TEXT_BACK.updateRequest = true;
  LEDS_TEXT_BACK.updated = false;
  cmdMessenger.sendCmd(kAcknowledge, "onSetBackTextColor triggered!");
}

void onSetBackCameraColor() {

  LEDS_CAMERA_BACK_COLOR.r = cmdMessenger.readInt16Arg();
  LEDS_CAMERA_BACK_COLOR.g = cmdMessenger.readInt16Arg();
  LEDS_CAMERA_BACK_COLOR.b = cmdMessenger.readInt16Arg();

  LEDS_CAMERA_BACK.updateRequest = true;
  LEDS_CAMERA_BACK.updated = false;

  cmdMessenger.sendCmd(kAcknowledge, "onSetBackCameraColor triggered!");
}

void onSetPrinterError() {

  bool errorState = cmdMessenger.readBoolArg();
  if ( errorState == true ) {

    LEDS_ERROR_STATE.updateRequest = true;
    LEDS_ERROR_STATE.updated = false;
    LEDS_ERROR_STATE.index = 0;

  }

  else {

    LEDS_ERROR_STATE.updateRequest = false;
    LEDS_ERROR_STATE.updated = false;
    LEDS_ERROR_STATE.index = 0;
    LEDS_FRONT.updateRequest = true;
    LEDS_SIDE_RIGHT.updateRequest = true;
    LEDS_SIDE_LEFT.updateRequest = true;
    LEDS_TEXT_BACK.updateRequest = true;
    LEDS_CAMERA_BACK.updateRequest = true;

  }

  Serial.println("onSetPrinterError command");
  cmdMessenger.sendCmd(kAcknowledge, "onSetPrinterError triggered!");

}

void onSetBrightness() {

  brightness = cmdMessenger.readInt16Arg();
  cmdMessenger.sendCmd(kAcknowledge, "onSetBrightness triggered!");

  LEDS_FRONT.updateRequest = true;
  LEDS_SIDE_RIGHT.updateRequest = true;
  LEDS_SIDE_LEFT.updateRequest = true;
  LEDS_TEXT_BACK.updateRequest = true;
  LEDS_CAMERA_BACK.updateRequest = true;

  LEDS_FRONT.updated == false;
  
}

void setup() {

  Serial.begin(115200);
  cmdMessenger.printLfCr();
  attachCommandCallbacks();
  onCommandList();
  strip.begin();
  cmdMessenger.sendCmd(kAcknowledge, "NodeMCU has started!");
}


void updateErrorLeds() {

  if (millis() > LEDS_ERROR_STATE.blinkingTimerMs ) {
    LEDS_ERROR_STATE.index = LEDS_ERROR_STATE.index + 1;
    int r, g, b;

    if ( LEDS_ERROR_STATE.index % 2 == 0) {
      r = LEDS_ERROR_COLOR_1.r;
      g = LEDS_ERROR_COLOR_1.g;
      b = LEDS_ERROR_COLOR_1.b;
    }
    else {
      r = LEDS_ERROR_COLOR_2.r;
      g = LEDS_ERROR_COLOR_2.g;
      b = LEDS_ERROR_COLOR_2.b;
    }

    Serial.print( "LEDS_ERROR_STATE_COLOR["); Serial.print(r, 16); Serial.print(g, 16); Serial.print(b, 16); Serial.println("]");
    for (int i = 0; i < frontRight[0]; i++)
      strip.setPixelColor(i, strip.Color(r, g, b));
    for (int i = frontLeft[1]; i < PixelCount; i++)
      strip.setPixelColor(i, strip.Color(r, g, b));

    LEDS_ERROR_STATE.blinkingTimerMs = millis() + LEDS_ERROR_STATE.blinkingDelayMs;
    LEDS_ERROR_STATE.updated = true;

  }

  LEDS_ERROR_STATE.updateRequest = true;

}

void updateFrontLeds() {

  if ( LEDS_FRONT.blinking == true ) {

    int n = millis() - LEDS_FRONT.timerMS;
    if ( n < 0 ) {

      if (millis() > LEDS_FRONT.blinkingTimerMs ) {
        LEDS_FRONT.index = LEDS_FRONT.index + 1;
        int r, g, b;

        if ( LEDS_FRONT.index % 2 == 0) {
          r = LEDS_FRONT_COLOR_1.r;
          g = LEDS_FRONT_COLOR_1.g;
          b = LEDS_FRONT_COLOR_1.b;
        }
        else {
          r = LEDS_FRONT_COLOR_2.r;
          g = LEDS_FRONT_COLOR_2.g;
          b = LEDS_FRONT_COLOR_2.b;
        }

        Serial.print( "LEDS_FRONT_COLOR["); Serial.print(r, 16); Serial.print(g, 16); Serial.print(b, 16); Serial.println("]");
        for (int i = frontRight[0]; i < frontRight[1]; i++)
          strip.setPixelColor(i, strip.Color(r, g, b));

        for (int i = frontLeft[0]; i < frontLeft[1]; i++)
          strip.setPixelColor(i, strip.Color(r, g, b));

        LEDS_FRONT.blinkingTimerMs = millis() + LEDS_FRONT.blinkingDelayMs;
        LEDS_FRONT.updated = true;


      }

      LEDS_FRONT.updateRequest = true;

    } else {

      LEDS_FRONT.blinking = false;

    }

  }

  else {

    int r = LEDS_FRONT_COLOR_1.r;
    int g = LEDS_FRONT_COLOR_1.g;
    int b = LEDS_FRONT_COLOR_1.b;

    for (int i = frontRight[0]; i < frontRight[1]; i++)
      strip.setPixelColor(i, strip.Color(r, g, b));

    for (int i = frontLeft[0]; i < frontLeft[1]; i++)
      strip.setPixelColor(i, strip.Color(r, g, b));

    LEDS_FRONT.updated = true;
    Serial.print( "LEDS_FRONT_COLOR["); Serial.print(r, 16); Serial.print(g, 16); Serial.print(b, 16); Serial.println("]");

  }

}

void updateRightSideLeds() {

  int r = LEDS_SIDE_RIGHT_COLOR.r;
  int g = LEDS_SIDE_RIGHT_COLOR.g;
  int b = LEDS_SIDE_RIGHT_COLOR.b;
  for (int i = sideRight[0]; i < sideRight[1]; i++)
    strip.setPixelColor(i,  strip.Color(r, g, b));
  LEDS_SIDE_RIGHT.updated = true;
  Serial.print( "LEDS_SIDE_RIGHT_COLOR["); Serial.print(r, 16); Serial.print(g, 16); Serial.print(b, 16); Serial.println("]");

}

void updateLeftSideLeds() {

  int r = LEDS_SIDE_LEFT_COLOR.r;
  int g = LEDS_SIDE_LEFT_COLOR.g;
  int b = LEDS_SIDE_LEFT_COLOR.b;
  for (int i = sideLeft[0]; i < sideLeft[1]; i++)
    strip.setPixelColor(i, strip.Color(r, g, b));
  LEDS_SIDE_LEFT.updated = true;
  Serial.print( "LEDS_SIDE_LEFT_COLOR["); Serial.print(r, 16); Serial.print(g, 16); Serial.print(b, 16); Serial.println("]");

}

void updateBackTextLeds() {

  int r = LEDS_TEXT_BACK_COLOR.r;
  int g = LEDS_TEXT_BACK_COLOR.g;
  int b = LEDS_TEXT_BACK_COLOR.b;
  for (int i = approchez[0]; i < approchez[1]; i++)
    strip.setPixelColor(i, strip.Color(r, g, b));

  for (int i = boxaselfi[0]; i < boxaselfi[1]; i++)
    strip.setPixelColor(i, strip.Color(r, g, b));
  LEDS_TEXT_BACK.updated = true;
  Serial.print( "LEDS_TEXT_BACK_COLOR["); Serial.print(r, 16); Serial.print(g, 16); Serial.print(b, 16); Serial.println("]");
}

void updateBackCameraLeds() {

  int r = LEDS_CAMERA_BACK_COLOR.r;
  int g = LEDS_CAMERA_BACK_COLOR.g;
  int b = LEDS_CAMERA_BACK_COLOR.b;
  for (int i = appareilphoto[0]; i < appareilphoto[1]; i++)
    strip.setPixelColor(i, strip.Color(r, g, b));
  LEDS_CAMERA_BACK.updated = true;
  Serial.print( "LEDS_CAMERA_BACK_COLOR["); Serial.print(r, 16); Serial.print(g, 16); Serial.print(b, 16); Serial.println("]");

}

void loop() {

  cmdMessenger.feedinSerialData();

  
  
  if (LEDS_FRONT.updateRequest) {
    LEDS_FRONT.updateRequest = false;
    updateFrontLeds();

  }
  if (LEDS_SIDE_RIGHT.updateRequest) {
    LEDS_SIDE_RIGHT.updateRequest = false;
    updateRightSideLeds();
  }
  if (LEDS_SIDE_LEFT.updateRequest) {
    LEDS_SIDE_LEFT.updateRequest = false;
    updateLeftSideLeds();
  }
  if (LEDS_TEXT_BACK.updateRequest) {
    LEDS_TEXT_BACK.updateRequest = false;
    updateBackTextLeds();
  }
  if (LEDS_CAMERA_BACK.updateRequest) {
    LEDS_CAMERA_BACK.updateRequest = false;
    updateBackCameraLeds();
  }
  if (LEDS_ERROR_STATE.updateRequest) {
    LEDS_ERROR_STATE.updateRequest = false;
    updateErrorLeds();
  }

  if (LEDS_FRONT.updated == true
      || LEDS_SIDE_RIGHT.updated == true
      || LEDS_SIDE_LEFT.updated == true
      || LEDS_TEXT_BACK.updated == true
      || LEDS_CAMERA_BACK.updated == true
      || LEDS_ERROR_STATE.updated == true ) {

    strip.setBrightness(brightness);
    strip.show();

    LEDS_FRONT.updated = true;
    LEDS_SIDE_RIGHT.updated = true;
    LEDS_SIDE_LEFT.updated = true;
    LEDS_TEXT_BACK.updated = true;
    LEDS_CAMERA_BACK.updated = true;
    LEDS_ERROR_STATE.updated = true;

  }

}
