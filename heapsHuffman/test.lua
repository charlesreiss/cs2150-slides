items = {
    {'b',1}, {'f',1}, {'m',1}, {'p',1}, {'u','1'},
    {',',1}, {'e',2}, {'o',2}, {'s',2}, {'i','5'},
    {'\\space','9'}
}

for k, v in pairs(items) do
    tex.sprint({
        "\\node[label={[font=\\small]north west:",
        v[2],
        "},font=\\tt\\small] {",
        v[1],
        "};} \\\\"
    })
end
