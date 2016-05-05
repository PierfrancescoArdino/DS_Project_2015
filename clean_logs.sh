#!/bin/bash
cd logs
if [ "$(ls -A )" ]; then
  rm *
fi
