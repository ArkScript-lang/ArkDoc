Rainbow.extend('arkscript', [
    {
        /* making peace with HTML */
        name: 'plain',
        pattern: /&gt;|&lt;/g
    },
    {
        name: 'comment',
        pattern: /#.*$/gm
    },
    {
        name: 'constant.language',
        pattern: /true|false|nil/g
    },
    {
        name: 'constant.symbol',
        pattern: /'[^()\s#']+/g
    },
    {
        name: 'constant.number',
        pattern: /\b\d+(?:\.\d*)?\b/g
    },
    {
        name: 'string',
        pattern: /".+?"/g
    },
    {
        matches: {
            1: 'storage.function',
            2: 'variable'
        },
        pattern: /\(\s*(let|mut|set)\s+\(?(\S+)/g
    },
    {
        matches: {
            1: 'keyword'
        },
        pattern: /\(\s*(begin|if|fun|quote|set|while|let|mut|del|import)(?=[\]()\s#])/g
    },
    {
        matches: {
            1: 'entity.function'
        },
        pattern: /\(\s*(=|<|>|<=|>=|!=|@|\^|\+|\-|\*|\/|tailOf|headOf|nil\?|list|len|append|concat|print|puts|input|time|empty\?|firstOf|assert|toNumber|toString|and|or|mod|type|hasField|not)(?=[\]()\s#])/g
    }
]);