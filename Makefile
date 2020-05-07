SRC_DIR = .\Source
INC_DIR = .\Include

#OBJS specifies which files to compile as part of the project
OBJS = $(wildcard $(SRC_DIR)/*.cpp)

#CC specifies which compiler we're using
CC = g++

#INCLUDE_PATHS specifies the additional include paths we'll need
INCLUDE_PATHS = -ID:\MinGW\include\SDL2 -I$(INC_DIR)

#LIBRARY_PATHS specifies the additional library paths we'll need
LIBRARY_PATHS = -LD:\MinGW\lib

#COMPILER_FLAGS specifies the additional compilation options we're using
# -w suppresses all warnings
# -Wl,-subsystem,windows gets rid of the console window
COMPILER_FLAGS = -w 

#LINKER_FLAGS specifies the libraries we're linking against
LINKER_FLAGS = -lmingw32 -lSDL2main -lSDL2 -lSDL2_Image

#OBJ_NAME specifies the name of our exectuable
OBJ_NAME = Build\TextWars

#This is the target that compiles our executable
all : $(OBJS)
	$(CC) $(OBJS) $(INCLUDE_PATHS) $(LIBRARY_PATHS) $(COMPILER_FLAGS) $(LINKER_FLAGS) -o $(OBJ_NAME)