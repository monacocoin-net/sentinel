#!/bin/bash
set -evx

mkdir ~/.monoeciCore

# safety check
if [ ! -f ~/.monoeciCore/.monoeci.conf ]; then
  cp share/monoeci.conf.example ~/.monoeciCore/monoeci.conf
fi
