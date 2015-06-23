# -*- coding: utf-8 -*-

__ACTIVATOR = '''#!/bin/bash

export HISTFILE=$ENVY_DIR/history
export PATH=$ENVY_DIR/macros:$ENVY_DIR/bin:$PATH
export PS1="${ENVY_PROMPT}${PS1}"
'''


# TODO: (Ironically) Migrate these programs to the new plugin infrastructure
__TODOS_MD = '''TODOS
=====

'''


__TODOS = '''#!/bin/bash
$EDITOR $ENVY_DIR/todos.md
'''


__RECORDING = '''#!/bin/bash

if (( $# != 1 )); then
    echo "Usage: record MACRO_NAME"
    exit 1
fi

export ENVY_MACRO_NAME=$1

rm -f ${ENVY_DIR}/macros/${ENVY_MACRO_NAME}

bash --init-file $ENVY_DIR/bin/recording_sub

sed -i '$ d' ${ENVY_DIR}/macros/${ENVY_MACRO_NAME}
chmod +x ${ENVY_DIR}/macros/${ENVY_MACRO_NAME}
'''


__RECORDING_SUB = '''#!/bin/bash
export PS1="${ENVY_PROMPT}${PS1}\\e[31m▣\\e[0m "
export HISTFILE=${ENVY_DIR}/macros/${ENVY_MACRO_NAME}

echo "Recording macro \\"${ENVY_MACRO_NAME}\\"; use \\"exit\\" to stop recording"
'''