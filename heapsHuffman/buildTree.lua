function buildTreeInitialSets()
    items = {
        {'b',1}, {'f',1}, {'m',1}, {'p',1}, {'u','1'},
        {',',1}, {'e',2}, {'o',2}, {'s',2}, {'i','5'},
        {'\\textvisiblespace','9'}
    }

    for k, v in pairs(items) do
        tex.sprint({
            "\\node[treeNode,label={[treeLabel]north west:",
            v[2],
            "}] (initial-", v[1], ") {",
            v[1],
            "}; \\& "
        })
    end
end

function buildSets(items, key)
    for k, v in pairs(items) do
        freq = v[3]
        value = v[2]
        nodeType = v[1]
        if nodeType == 'single' then
            tex.sprint({
                "\\node[treeNode,label={[treeLabel]north west:",
                freq,
                "}] (", key, "-", value, ") {",
                value,
                "}; \\& "
            })
        else
            tex.sprint({
                "\\node[graphContainer,label={[graphContainerLabel]north west:", freq,
                "}] (", key, "-", v[4], ") {",
                "\\begin{tikzpicture}\\begin{scope}[treeSubGraph]",
                "\\graph {",
                value,
                "};\\end{scope}\\end{tikzpicture}",
                "}; \\&",
            })
        end
    end
end

function buildTreeSecondSets()
    items = {
        {'single', 'm', 1}, {'single', 'p', 1}, {'single', 'u', 1}, {'single', ',',1},
        {'graph', '/ -> {b,f}', 2, 'bf'}, 
        {'single', 'e',2}, {'single', 'o',2}, {'single', 's',2}, {'single', 'i','5'},
        {'single', '\\textvisiblespace','9'}
    }
    buildItems(items, 'second')
end
