'''
I pay 1951.28
Total is 8457.70
I need to cash out $6506.42
'''
nick_lippis = {
    'nick': {
        'amount': -1961.28,
        'phone': '16178271991',
    }
}
zack_morris = {
    'zmo': {
        'amount': -876.29,
        'phone': '15308591050',
    }
}
cynthia_laiacona = {
    'cyn': {
        'amount': -1716.28,
        'phone': '15308590976',
    }
}
kyle_merwin = {
    'kyle': {
        'amount': -976.29,
        'phone': '14157204626',
    }
}
rob_garbanati = {
    'rob': {
        'amount': -976.28,
        'phone': '19496331541',
    }
}
nate_siswanto = {
    'nate': {
        'amount': -876.29,
        'phone': '18186319598',
    }
}

# 2/31 for Cyn
# $500 for Ben Hunter
temp_ben_hunter = {
    'ben_hunter': {
        'amount': -500,
        'phone': '14153422879',
    }
}
roommates = {}
for roommate in [kyle_merwin,
                 nick_lippis,
                 rob_garbanati,
                 zack_morris,
                 temp_ben_hunter]:
    roommates.update(roommate)
