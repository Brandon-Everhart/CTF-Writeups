
import angr

proj = angr.Project('./nice_try', load_options={"auto_load_libs":False})
initial_state = proj.factory.entry_state() 
initial_state.options.discard("LAZY_SOLVES")

k = initial_state.posix.files[0].read_from(6)
initial_state.se.add(k == 'intro{')

for _ in range(6,53):
	k = initial_state.posix.files[0].read_from(1)
	initial_state.se.add(k != 0)
	initial_state.se.add(k != 10)

k = initial_state.posix.files[0].read_from(1)
initial_state.se.add(k == 10)

initial_state.posix.files[0].seek(0)
initial_state.posix.files[0].length = 54

pg = proj.factory.path_group(initial_state, immutable=False)
print("Exploring...")
pg.explore(find= 0x5610da61bbe8)
print pg
#print pg.errored[0].error
#print pg.errored[1].error
#print pg.errored[2].error

found = pg.found[0].state
found.posix.files[0].seek(0)
print("Found: "+ found.se.any_str(found.posix.files[0].read_from(54)))
#print found

'''
ecx = 

edx = 0x51eb851f
edx = edx * edx
edx = edx/(2*5)


 0x00400753
 dr eax

1804289383 
846930886   
1681692777 
1714636915
1957747793
424238335
719885386
1649760492
596516649
1189641421

'''