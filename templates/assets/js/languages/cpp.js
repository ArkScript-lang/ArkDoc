Rainbow.extend("cpp", [
    {
        name: "meta.preprocessor",
        matches: {
            1: [
                { matches: { 1: "keyword.define", 2: "entity.name" }, pattern: /(\w+)\s(\w+)\b/g },
                { name: "keyword.define", pattern: /endif/g },
                { name: "constant.numeric", pattern: /\d+/g },
                { matches: { 1: "keyword.include", 2: "string" }, pattern: /(include)\s(.*?)$/g },
            ],
        },
        pattern: /\#([\S\s]*?)$/gm,
    },
    { name: "keyword", pattern: /\b(while|break|continue|switch|case|default|do|goto|typedef|template|decltype|delete|if|else|for|nullptr|operator|namespace|new|this|try|except|typename|sizeof|throw|typeid|using)\b/g },
    { matches: { 1: "storage.type", 3: "storage.type", 4: "entity.name.function" }, pattern: /\b((un)?signed|const)? ?(void|char|short|int|long|float|double)\*? +((\w+)(?= ?\())?/g },
    { matches: { 2: "entity.name.function" }, pattern: /(\w|\*) +((\w+)(?= ?\())/g },
    { name: "storage.modifier", pattern: /\b(static|extern|auto|register|volatile|inline|constexpr|explicit|export|mutable|private|protected|public|virtual|final|override)\b/g },
    { name: "support.type", pattern: /\b(struct|union|enum|class)\b/g },
    { name: "support.namespace", pattern: /([A-Za-z_]+::)+[A-Za-z_]+/g, },
    {
        matches: {
            1: "function.method.call",
        },
        pattern: /([A-Za-z_]+\.)[A-Za-z_]+(?=\))/g,
    },
], 'generic');