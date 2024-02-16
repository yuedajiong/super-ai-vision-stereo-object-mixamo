def main(path_root='../data/mixamo/', real_remove=1):
    import os
    for path_c in sorted(os.listdir(path_root)):
        for file_a in sorted(os.listdir(os.path.join(path_root, path_c))):
            indexA = file_a.find(' (')
            indexZ = file_a.find(').')
            if indexA>=0 and indexZ>=indexA+1:
                this_name = os.path.join(path_root, path_c, file_a)
                base_name = os.path.join(path_root, path_c, file_a[0:indexA]+'.fbx')
                if not os.path.exists(this_name):
                    continue
                else:
                    this_size = os.path.getsize(this_name)
                    base_size = os.path.getsize(base_name)
                    if this_size == base_size:
                        print('$$$ kill by base:' + this_name, this_size, base_size)
                        if real_remove: os.remove(this_name)
                    else:
                        p = int(file_a[indexA+2:indexZ])
                        while(True): 
                            p = p+1               
                            peer_name = os.path.join(path_root, path_c, file_a[0:indexA]+' ('+str(p)+')'+'.fbx')   
                            if not os.path.exists(peer_name) and p>33:
                                break
                            else:
                                if this_name != peer_name and os.path.exists(this_name):
                                    if os.path.exists(peer_name):
                                        peer_size = os.path.getsize(peer_name)
                                        if this_size == peer_size:
                                            print('$$$ kill by peer:' + this_name, this_size, peer_size)
                                            if real_remove: os.remove(this_name)
                                        else:
                                            #print('$$$ ???? by peer:' + this_name, this_size, peer_size)
                                            continue
                                    else:
                                        continue
                                else:
                                    continue


if __name__ == '__main__':
    main()

