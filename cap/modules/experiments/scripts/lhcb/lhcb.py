# -*- coding: utf-8 -*-
#
# This file is part of CERN Analysis Preservation Framework.
# Copyright (C) 2016 CERN.
#
# CERN Analysis Preservation Framework is free software; you can redistribute
# it and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Analysis Preservation Framework is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Analysis Preservation Framework; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

import json
import os
import shelve

filenames = [
    "dbases/charm.shelve",
    "dbases/b2cc.shelve",
    "dbases/bandq.shelve",
    # "dbases/citations_cache.shelve",
    "dbases/qee.shelve",
    "dbases/sl.shelve",
    "dbases/b2oc.shelve",
    "dbases/bnoc.shelve",
    "dbases/hlt.shelve",
    "dbases/rd.shelve"
]

def dump_analyses_to_json():
    base = {}
    tmp_title_list = []
    home_dir = os.path.dirname(os.path.abspath(__file__))

    os.chdir(home_dir)

    # Create dir for jsonschemas if doesnt exist
    output_dir = '../../static/jsonschemas/fields'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in filenames:
        base_field = "analysis"
    
        title_list = []
    
        s = shelve.open(filename)
    
        # Get list of "title" for Anal.Name Autocomplete
        title_list = s.get('analysis').keys()
        for n in title_list:
            tmp_title_list.append({"value": n})
    
        working_group = filename.split("/")[1]
        working_group = working_group.replace(".shelve", "")
    
        with open('../../static/jsonschemas/fields/lhcb_ana_titles_'+working_group+'.json', 'w') as fp:
            json.dump(tmp_title_list, fp)
    
        def resolveObj(s, f, k):
            newk = {}
            for p in s[f][k]:
                if (hasattr(s[f][k][p], '__iter__')):
                    newp = {}
                    for l in s[f][k][p]:
                        try:
                            newp[l] = s[p][l]
                        except:
                            newk[p] = s[f][k][p]
                            break
                    newk[p] = newp
                else:
                    newk[p] = s[f][k][p]
            return newk
    
    
        for k in s.get(base_field):
            if not k in base:
                base[k] = resolveObj(s,base_field, k)
    
        s.close()
    
    with open('../../static/jsonschemas/fields/lhcb_ana_titles.json', 'w') as fp:
        json.dump(tmp_title_list, fp)
    
    with open('../../scripts/analyses.json', 'w') as fp:
        json.dump(base, fp, ensure_ascii=False)


if __name__=='__main__':
    dump_analyses_to_json()
