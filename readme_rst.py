import pypandoc

output = pypandoc.convert('README.md', 'rst')
rst = open('README.rst', 'w')
rst.write(output)
rst.close()