# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import curses

# cheating was a dict(generator comprehension)
bla = {'KEY_BREAK': 257, 'KEY_DOWN': 258, 'KEY_UP': 259, 'KEY_LEFT': 260, 'KEY_RIGHT': 261, 'KEY_HOME': 262, 'KEY_BACKSPACE': 263, 'KEY_F0': 264, 'KEY_F1': 265, 'KEY_F2': 266, 'KEY_F3': 267, 'KEY_F4': 268, 'KEY_F5': 269, 'KEY_F6': 270, 'KEY_F7': 271, 'KEY_F8': 272, 'KEY_F9': 273, 'KEY_F10': 274, 'KEY_F11': 275, 'KEY_F12': 276, 'KEY_F13': 277, 'KEY_F14': 278, 'KEY_F15': 279, 'KEY_F16': 280, 'KEY_F17': 281, 'KEY_F18': 282, 'KEY_F19': 283, 'KEY_F20': 284, 'KEY_F21': 285, 'KEY_F22': 286, 'KEY_F23': 287, 'KEY_F24': 288, 'KEY_F25': 289, 'KEY_F26': 290, 'KEY_F27': 291, 'KEY_F28': 292, 'KEY_F29': 293, 'KEY_F30': 294, 'KEY_F31': 295, 'KEY_F32': 296, 'KEY_F33': 297, 'KEY_F34': 298, 'KEY_F35': 299, 'KEY_F36': 300, 'KEY_F37': 301, 'KEY_F38': 302, 'KEY_F39': 303, 'KEY_F40': 304, 'KEY_F41': 305, 'KEY_F42': 306, 'KEY_F43': 307, 'KEY_F44': 308, 'KEY_F45': 309, 'KEY_F46': 310, 'KEY_F47': 311, 'KEY_F48': 312, 'KEY_F49': 313, 'KEY_F50': 314, 'KEY_F51': 315, 'KEY_F52': 316, 'KEY_F53': 317, 'KEY_F54': 318, 'KEY_F55': 319, 'KEY_F56': 320, 'KEY_F57': 321, 'KEY_F58': 322, 'KEY_F59': 323, 'KEY_F60': 324, 'KEY_F61': 325, 'KEY_F62': 326, 'KEY_F63': 327, 'KEY_DL': 328, 'KEY_IL': 329, 'KEY_DC': 330, 'KEY_IC': 331, 'KEY_EIC': 332, 'KEY_CLEAR': 333, 'KEY_EOS': 334, 'KEY_EOL': 335, 'KEY_SF': 336, 'KEY_SR': 337, 'KEY_NPAGE': 338, 'KEY_PPAGE': 339, 'KEY_STAB': 340, 'KEY_CTAB': 341, 'KEY_CATAB': 342, 'KEY_ENTER': 343, 'KEY_SRESET': 344, 'KEY_RESET': 345, 'KEY_PRINT': 346, 'KEY_LL': 347, 'KEY_A1': 348, 'KEY_A3': 349, 'KEY_B2': 350, 'KEY_C1': 351, 'KEY_C3': 352, 'KEY_BTAB': 353, 'KEY_BEG': 354, 'KEY_CANCEL': 355, 'KEY_CLOSE': 356, 'KEY_COMMAND': 357, 'KEY_COPY': 358, 'KEY_CREATE': 359, 'KEY_END': 360, 'KEY_EXIT': 361, 'KEY_FIND': 362, 'KEY_HELP': 363, 'KEY_MARK': 364, 'KEY_MESSAGE': 365, 'KEY_MOVE': 366, 'KEY_NEXT': 367, 'KEY_OPEN': 368, 'KEY_OPTIONS': 369, 'KEY_PREVIOUS': 370, 'KEY_REDO': 371, 'KEY_REFERENCE': 372, 'KEY_REFRESH': 373, 'KEY_REPLACE': 374, 'KEY_RESTART': 375, 'KEY_RESUME': 376, 'KEY_SAVE': 377, 'KEY_SBEG': 378, 'KEY_SCANCEL': 379, 'KEY_SCOMMAND': 380, 'KEY_SCOPY': 381, 'KEY_SCREATE': 382, 'KEY_SDC': 383, 'KEY_SDL': 384, 'KEY_SELECT': 385, 'KEY_SEND': 386, 'KEY_SEOL': 387, 'KEY_SEXIT': 388, 'KEY_SFIND': 389, 'KEY_SHELP': 390, 'KEY_SHOME': 391, 'KEY_SIC': 392, 'KEY_SLEFT': 393, 'KEY_SMESSAGE': 394, 'KEY_SMOVE': 395, 'KEY_SNEXT': 396, 'KEY_SOPTIONS': 397, 'KEY_SPREVIOUS': 398, 'KEY_SPRINT': 399, 'KEY_SREDO': 400, 'KEY_SREPLACE': 401, 'KEY_SRIGHT': 402, 'KEY_SRSUME': 403, 'KEY_SSAVE': 404, 'KEY_SSUSPEND': 405, 'KEY_SUNDO': 406, 'KEY_SUSPEND': 407, 'KEY_UNDO': 408, 'KEY_MOUSE': 409, 'KEY_RESIZE': 410, 'KEY_MIN': 257, 'KEY_MAX': 511}
#vars(curses).items()
CODE_TO_CHAR = {i: chr(i) for i in range(256)}
CODE_TO_CHAR.update({value: name[4:] for name, value in bla.items()
# cheating                    if name.startswith('KEY_')
})
# special exceptions
CODE_TO_CHAR[10] = 'ENTER'

CHAR_TO_CODE = {v: k for k, v in CODE_TO_CHAR.items()}
