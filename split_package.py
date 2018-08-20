#!/usr/bin/env python3

import argparse
import csv
import os
import subprocess
import sys
import math

"""
Edited 2018-06-18 by R Dickson (@rebeckson)
Download this script and make it executable. Usage example:

   $ ./split_sip.py \
       --prefix="Foobar_" \
       /var/archivematica/automation-sources/very-big-source/Foobar/Foobar-SIP/ \
       /var/archivematica/automation-sources/very-big-source/Foobar/Foobar-SIP-splitted/

The original location is not modified. Preferably run locally. It's been tested over NFS. It uses rsync so if you run it twice the files won't be copied again unless they don't match (rsync provides multiple matching algorithms).

Make sure that you have permissions on the locations you are reading or writing!
"""

class SIPMetadata(object):
    def __init__(self, source_sip, csv_delimiter):
        self.csv_file = os.path.join(source_sip, 'metadata', 'metadata.csv')
        self.csv_delimiter = csv_delimiter
        self.index_csv()

    def index_csv(self):
        self.index = dict()
        with open(self.csv_file, 'rt') as csvf:
            csvr = csv.reader(csvf, delimiter=self.csv_delimiter)
            for i, row in enumerate(csvr):
                if i == 0:
                    self.headers = row
                    continue
                path = row[0]
                self.index[path] = row

    def get_object_metadata(self, path):
        return (self.headers, self.index[path])


def rsync(src, dst, verbose=False):
    print('Copying objects... [src={}] [dst={}]'.format(src, dst))
    subprocess.check_call(['rsync', '-a', src, dst])


def main(source_sip, target_dir, csv_delimiter, max_objects=100, prefix=None):
    metadata = SIPMetadata(source_sip, csv_delimiter)
    objects_edited_dir = os.path.abspath(os.path.join(source_sip, 'objects', 'edited'))
    objects_unedited_dir = os.path.abspath(os.path.join(source_sip, 'objects', 'unedited'))
    target_dir = os.path.abspath(target_dir)
    max_objects = max_objects

    # List of directories under objects/
    objects_edited_dirs = os.listdir(objects_edited_dir)
    objects_unedited_dirs = os.listdir(objects_unedited_dir)
    if len(objects_edited_dirs) < 1:
        print('Edited object directory is empty: {}'.format(objects_edited_dir))

    # Case 1: Number of objects in edited folder exceeds max supplied by user. Split the package.
    elif len(objects_edited_dirs) > max_objects:


        # Determine number of packages
        num_packages = math.ceil(float(len(objects_edited_dirs))/float(max_objects))
        print('Transfer will be split into ' + str(num_packages) + ' packages:')

        # Create package folders 
        package_num = 1
        package_dirs = []
        while package_num <= num_packages:
            package_dir = 'package' if prefix is None else prefix + '{:02d}'.format(package_num)
            package_path = os.path.join(target_dir, package_dir)
            package_dirs.append(package_path)
            print("make", package_path)

            # Transfer submission docs
            sdoc_dir_src = os.path.join(source_sip, 'metadata', 'submissionDocumentation', '')
            sdoc_dir_dst = os.path.join(package_path, 'metadata', 'submissionDocumentation', '')
            try:
                os.makedirs(sdoc_dir_dst)
                print("make", sdoc_dir_dst)
            except OSError:
                pass
            rsync(sdoc_dir_src, sdoc_dir_dst, verbose=True)
            print('\033[92m{}: {}\033[00m'.format('submissionDocumentation should be available at', sdoc_dir_dst))
            
            package_num += 1


        # Move objects into packages
        package_index = 0
        objects_packaged = 0

        for i, item in enumerate(objects_edited_dirs):
            print('- {}'.format(item))
            # object folders
            src_edited = os.path.join(objects_edited_dir, item, '')
            src_unedited = os.path.join(objects_unedited_dir, item, '')

            if objects_packaged == max_objects:
            	package_index += 1
            	objects_packaged = 0

            target_package = package_dirs[package_index]
            dst_edited_objects = os.path.join(target_package, 'objects', 'edited', item, '')
            dst_unedited_objects = os.path.join(target_package, 'objects', 'unedited', item, '')
            dst_metadata = os.path.join(target_package, 'metadata', '')
            for dst in (dst_edited_objects, dst_unedited_objects, dst_metadata):
                try:
                    os.makedirs(dst)
                    print("make", dst)
                except OSError:
                    pass

            rsync(src_edited, dst_edited_objects)
            rsync(src_unedited, dst_unedited_objects)

            objects_packaged += 1

            # Split metadata
            try:
                headers, mdata = metadata.get_object_metadata('objects/edited/{}'.format(item))
            except KeyError:
                print('No metadata for {}'.format(item))
            else:
                print('Writing metadata...')
                csv_file = os.path.join(dst_metadata, 'metadata.csv')
                file_exists = os.path.isfile(csv_file)
                with open(csv_file, 'a') as csvf:
                    csvw = csv.writer(csvf)
                    if not file_exists:
                        csvw.writerow(headers)
                    csvw.writerow(mdata)
                    

    # Case 2: Number of objects in /edited is less than the user-supplied maximum. Don't split.    
    else:
        print("Not over max object limit. No need to split!")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('source_sip')
    parser.add_argument('target_dir')
    parser.add_argument('--max_objects', type=int, default=100)
    parser.add_argument('--csv-delimiter', type=str, default=',')
    parser.add_argument('--prefix', type=str, default=',')
    args = parser.parse_args()
    sys.exit(main(args.source_sip, args.target_dir, args.csv_delimiter, args.max_objects, args.prefix))