# -*- coding: utf-8 -*-

__ACTIVATOR = '''
#!/bin/bash

export HISTFILE=$ENVY_DIR/history
export PATH=$ENVY_DIR:$ENVY_SYS_DIR:$PATH
export PS1="${ENVY_PROMPT}${PS1}"
'''