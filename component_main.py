'''

Created on May 12, 2014

@author: dgrewal

component for titan pipeline
Run Titan
'''

from kronos.utils import ComponentAbstract
import os
#from components import io_manager as IOManager

class Component(ComponentAbstract):

    def __init__(self,component_name='run_titan', component_parent_dir=None, seed_dir=None):
        self.version = '1.1.5'
        ## initialize ComponentAbstract
        super(Component, self).__init__(component_name, component_parent_dir, seed_dir)

    def make_cmd(self,chunk=None):
        path = os.path.join(self.seed_dir, 'titan.R')

        cmd = ' '.join([self.requirements['R']+'script', path])
        
        if chunk is not None:
            params = eval(chunk)
            num_clusters = params['num_clusters']
            ploidy = params['ploidy']
        else:
            num_clusters = self.args.num_clusters
            ploidy = self.args.ploidy

        if self.args.chromosomes:
            if type(self.args.chromosomes) is not list: 
                raise Exception('Chromosomes should be list')
            chr = ["'"+str(val)+"'" for val in self.args.chromosomes]

            chr = '"c('+ ','.join(chr)+')"'
        else:
            chr = "NULL"

        #couldn't iterate as the order isn't preserved in args object
        cmd_args = [self.args.id, self.args.infile, self.args.cnfile,
                    self.args.map, num_clusters, self.args.num_cores,
                    ploidy, self.args.outfile, self.args.outparam,
                    self.args.myskew, self.args.bool_est_ploidy, self.args.n_zero,
                    self.args.norm_est_meth, self.args.max_i, self.args.pseudo_counts,
                    self.args.txn_exp_len, self.args.txn_z_strength, self.args.alpha_k,
                    self.args.alpha_high,self.args.maxcn,self.args.sym,
                    self.args.obj_outfile, self.args.genome_type, chr,
                    self.args.y_threshold]

        return cmd,cmd_args

    def test(self):
        import component_test
        component_test.run()

def _main():
    comp = Component()
    comp.test()
    comp.args = component_ui.args
    comp.run()

if __name__ == '__main__':
    import component_ui
    _main()
