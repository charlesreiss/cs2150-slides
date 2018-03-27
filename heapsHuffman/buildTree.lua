function buildTreeInitialSets()
    items = {
        {'b',1}, {'f',1}, {'m',1}, {'p',1}, {'u','1'},
        {',',1,'comma'}, {'e',2}, {'o',2}, {'s',2}, {'i','5'},
        {'\\textvisiblespace','9', 'space'}
    }

    for k, v in pairs(items) do
        name = v[3]
        if name == nil then
            name = v[1]
        end
        tex.sprint({
            "\\node[treeNode,label={[treeLabel]north west:",
            v[2],
            "}] ", "(initial-" .. name .. ")", " {",
            v[1],
            "}; \\& "
        })
    end
end

function buildItems(items, key)
    for k, v in pairs(items) do
        freq = v[3]
        value = v[2]
        value = string.gsub(value, "\n", "")
        nodeType = v[1]
        name = v[4]
        if name == nil then
            name = value
        end
        if nodeType == 'single' then
            tex.sprint({
                "\\node[treeNode,label={[treeLabel]north west:",
                freq,
                "}] (" .. key .. "-" .. name .. ") {",
                value,
                "}; \\& "
            })
        else
            tex.sprint({
                "\\node[graphContainer,label={[graphContainerLabel]north west:", freq,
                "}] (" .. key .. "-" .. name .. ") {",
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
        {'single', 'm', 1}, {'single', 'p', 1}, {'single', 'u', 1}, {'single', ',',1, 'comma'},
        {'graph', '/ -> {b[> "0"\'],f[> "1"]}', 2, 'bf'}, 
        {'single', 'e',2}, {'single', 'o',2}, {'single', 's',2}, {'single', 'i','5'},
        {'single', '\\textvisiblespace','9', 'space'}
    }
    buildItems(items, 'second')
end
function buildTreeThirdSets()
    items = {
        {'single', 'u', 1}, {'single', ',',1, 'comma'},
        {'graph', '/ -> {m[> "0"\'],p[> "1"]}', 2, 'mp'}, 
        {'graph', '/ -> {b[> "0"\'],f[> "1"]}', 2, 'bf'}, 
        {'single', 'e',2}, {'single', 'o',2}, {'single', 's',2},
        {'single', 'i','5'},
        {'single', '\\textvisiblespace','9', 'space'}
    }
    buildItems(items, 'third')
end
function buildTreeFourthSets()
    items = {
        {'graph', '/ -> {u[> "0"\'],comma[as={,},> "1"]}', 2, 'ucomma'}, 
        {'graph', '/ -> {m[> "0"\'],p[> "1"]}', 2, 'mp'}, 
        {'graph', '/ -> {b[> "0"\'],f[> "1"]}', 2, 'bf'}, 
        {'single', 'e',2}, {'single', 'o',2}, {'single', 's',2},
        {'single', 't','4'},
        {'single', 'i','5'},
        {'single', '\\textvisiblespace','9', 'space'}
    }
    buildItems(items, 'fourth')
end
function buildTreeFifthSets()
    items = {
        {'graph', '/ -> {b[> "0"\'],f[> "1"]}', 2, 'bf'}, 
        {'single', 'e',2}, {'single', 'o',2}, {'single', 's',2},
        {'graph', '/ -> {/[> "0"\'] -> {u[> "0"\'],comma[as={,},> "1"]}, /[> "1"] ->  {m[> "0"\'],p[> "1"]}}', 4, 'ucommamp'}, 
        {'single', 't','4'},
        {'single', 'i','5'},
        {'single', '\\textvisiblespace','9', 'space'}
    }
    buildItems(items, 'fifth')
end
function buildTreeFifthBSets()
    items = {
        {'graph', '/ -> {u[> "0"\'],comma[as={,},> "1"]}', 2, 'ucomma'}, 
        {'graph', '/ -> {b[> "0"\'],f[> "1"]}', 2, 'bf'}, 
        {'single', 'e',2}, {'single', 's',2}, 
        {'graph', '/ -> {o[> "0"\'], / -> {m[> "0"\'],p[> "1"]}}', 3, 'mpo'},
        {'single', 't','4'},
        {'single', 'i','5'},
        {'single', '\\textvisiblespace','9', 'space'}
    }
    buildItems(items, 'fifthB')
end
function buildTreeSeventhSets()
    items = {
        {'graph', '/ -> {/[> "0"\'] -> {b[> "0"\'],f[> "1"]}, e[> "1"]}', 4, 'bfe'}, 
        {'graph', '/ -> {o[> "0"\'],s[> "1"]}', 4, 'os'}, 
        {'graph', '/ -> {/[> "0"\'] -> {u[> "0"\'],comma[as={,},> "1"]}, /[> "1"] ->  {m[> "0"\'],p[> "1"]}}', 4, 'ucommamp'}, 
        {'single', 't','4'},
        {'single', 'i','5'},
        {'single', '\\textvisiblespace','9', 'space'}
    }
    buildItems(items, 'seventh')
end
function buildTreeNinthSets()
    items = {
        {'single', 'i','5'},
        {'graph', [[
            [fresh nodes] / -> {
                /[> "0"'] -> {/[> "0"'] -> {b[> "0"'], f[> "1"]}, e[> "1"]},
                /[> "1"] -> {o[> "0"'], s[> "1"]}
            }
        ]], 8, 'bfeos'}, 
        {'graph', [[
            [fresh nodes] / -> {
                /[> "0"'] -> {
                    /[> "0"'] -> {u[> "0"'],comma[as={,},> "1"]},
                    /[> "1"] ->  {m[> "0"'],p[> "1"]}
                },
                t[> "1"]
            }
        ]], 9, 'ucommampt'}, 
        {'single', '\\textvisiblespace','9', 'space'}
    }
    buildItems(items, 'ninth')
end

function buildTreeTenthSets()
    items = {
        {'graph', [[
            [fresh nodes] / -> {
                /[> "0"'] -> {
                    /[> "0"'] -> {u[> "0"'],comma[as={,},> "1"]},
                    /[> "1"] ->  {m[> "0"'],p[> "1"]}
                },
                t[> "1"]
            }
        ]], 9, 'ucommampt'}, 
        {'single', '\\textvisiblespace','9', 'space'},
        {'graph', [[
            [fresh nodes] / -> {
                /[> "0"'] -> {
                    /[> "0"'] -> {/[> "0"'] -> {b[> "0"'], f[> "1"]}, e[> "1"]},
                    /[> "1"] -> {o[> "0"'], s[> "1"]}
                },
                i[> "1"]
            }
        ]], 13, 'ibfeos'},
    }
    buildItems(items, 'tenth')
end

function buildTreeEleventhSets()
    items = {
        {'graph', [[
            [fresh nodes] / -> {
                space[> "0"',as={\textvisiblespace}],
                /[> "1"] -> {
                    /[> "0"'] -> {
                        /[> "0"'] -> {u[> "0"'],comma[as={,},> "1"]},
                        /[> "1"] ->  {m[> "0"'],p[> "1"]}
                    },
                    t[> "1"]
                }
            }
        ]], 18, 'spaceucommampt'}, 
        {'graph', [[
            [fresh nodes] / -> {
                /[> "0"'] -> {
                    /[> "0"'] -> {/[> "0"'] -> {b[> "0"'], f[> "1"]}, e[> "1"]},
                    /[> "1"] -> {o[> "0"'], s[> "1"]}
                },
                i[> "1"]
            }
        ]], 13, 'ibfeos'}, 
    }
    buildItems(items, 'eleventh')
end

function buildTreeFinalSets()
    items = {
        {'graph', [[
            [fresh nodes] / -> {
                 /[> "0"'] -> {
                    space[as={\textvisiblespace},> "0"'],
                    /[> "1"] -> {
                        /[> "0"'] -> {
                            /[> "0"'] -> {u[> "0"'],comma[as={,},> "1"]},
                            /[> "1"] ->  {m[> "0"'],p[> "1"]}
                        },
                        t[> "1"]
                    }
                },
                /[> "1"] ->  {
                    /[> "0"'] -> {
                        /[> "0"'] -> {/[> "0"'] -> {b[> "0"'], f[> "1"]}, e[> "1"]},
                        /[> "1"] -> {o[> "0"'], s[> "1"]}
                    },
                    i[> "1"]
                }
            }
        ]], 31, 'all'}
    }
    buildItems(items, 'final')
end
