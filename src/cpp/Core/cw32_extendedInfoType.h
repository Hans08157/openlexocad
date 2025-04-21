#pragma once

typedef struct CodeExtendedInfoType
{
  char displayName[63 + 1];
  char SW_ID[16 + 1];
  char LicenseName[32 + 1];
  char Code_Valid[60 + 1];
  char CODE_NORM[60 + 1];
  char CODE_DEMO[60 + 1];
  char OPTION[128 + 1];
  char OPTION2[128 + 1];
  int NB_DAY_UNTIL_EXPIRATION;
  char DATE_LIM[9];
  char Node_Dir[260];
  int floatingLicense;
  int dataValid;
  int webLicense;

  int errValue;

  struct LexoCodeInfo *lexoCodeInfo;

} CodeExtendedInfoType;


