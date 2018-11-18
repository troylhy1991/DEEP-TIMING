PROJECT(Preprocessing)

cmake_minimum_required(VERSION 2.0)

if(COMMAND cmake_policy)
  cmake_policy(SET CMP0003 NEW)
endif(COMMAND cmake_policy)

find_package(ITK REQUIRED)
include(${ITK_USE_FILE})

# adding a library
ADD_LIBRARY(helper helpers.cpp helpers.h)
TARGET_LINK_LIBRARIES(helper ${ITK_USE_LIBRARIES})

# linear unmixing:
ADD_EXECUTABLE(rescale rescale.cpp )
TARGET_LINK_LIBRARIES(rescale helper ${ITK_LIBRARIES})


