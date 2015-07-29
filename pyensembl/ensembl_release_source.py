# Copyright (c) 2015. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .genome_source import GenomeSource


class EnsemblReleaseSource(GenomeSource):
    """
    Represents a URL or local file path of a GTF or FASTA file
    within an Ensembl release. Also handles some Ensembl-specific
    local filename transformation and generates Ensembl-specific
    install messages.
    """
    def __init__(self, name, path_or_url):
        GenomeSource.__init__(
            self,
            name=name,
            path_or_url=path_or_url)

    @property
    def original_filename(self):
        original_filename = super(EnsemblReleaseSource, self).original_filename
        assert original_filename.endswith(".gtf.gz"), \
            "Expected remote GTF file %s to end with '.gtf.gz'" % (
                original_filename)
        return original_filename

    @property
    def cached_filename(self):
        """
        We sometimes need to add the release number to a cached FASTA filename
        since some Ensembl releases only have the genome name in the FASTA
        filename but still differ subtly between releases.
        For example, a transcript ID may be missing in Ensembl 75 but present
        in 76, though both have the same FASTA filename
        """
        if ".%d." % self.release in self.original_filename:
            return self.original_filename

        filename_parts = self.original_filename.split(".fa.")
        assert len(filename_parts) == 2, \
            "Expected remote filename %s to contain '.fa.gz'" % (
                self.original_filename,)
        return "".join([
            filename_parts[0],
            ".%d.fa." % self.release,
            filename_parts[1]])

    def install_string_console(self):
        return "pyensembl install --release %d" % self.release

    def install_string_python(self):
        return "EnsemblRelease(%d).install()" % self.release

    def __str__(self):
        return "EnsemblReleaseSource(%s)" % self._arg_list_str()

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (
            other.__class__ is EnsemblReleaseSource and
            self.paths == other.paths)

    def __hash_(self):
        return hash((self.paths))
