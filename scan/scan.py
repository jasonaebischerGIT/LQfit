import treemodels
import randompar
import parameterscan
import logging
import argparse


logging.basicConfig(level=logging.DEBUG)


def _get_model_point(par):
    """Get a treemodels model point from a parameter dict"""
    p = par.copy()
    scale = p.pop('scale')
    return treemodels.ModelPoint(p, scale)

def obsfunc(par):
    """Function for the 'observables' table.

    Simply takes the `theory` column of the obstable.
    """
    mp = _get_model_point(par)
    pp = mp.global_likelihood
    df = pp.obstable()
    return df['theory']

def llfunc(par):
    """Function for the 'log_likelihood' table.

    Saves smelli's log_likelihood_dict.
    """
    mp = _get_model_point(par)
    pp = mp.global_likelihood
    return pp.log_likelihood_dict()


# dictionary where each key will become a table in the SQL database
funcdic = {
    'observables': obsfunc,
    'log_likelihood': llfunc,
}



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Scalar leptoquark random scan.")
    parser.add_argument("-s", type=int, default=8,
                        help="Batch size (number of points per batch, default 8)")
    parser.add_argument("-b", type=int, default=1,
                        help="Number of batches (default 1)")
    parser.add_argument("-t", type=int, default=1,
                        help="Number of threads (default 1)")
    args = parser.parse_args()

    def parfunc():
        """Return random parameter dict in the right format"""
        _d = randompar.random_omega1()
        d  = _d['p']
        d['scale'] = _d['scale']
        return d
    logging.info("Starting scan for model omega1 with {} batches of {}"
                 .format(args.b, args.s))
    store = parameterscan.ScanStoreSQL('omega1')
    scan = parameterscan.RandomScan(store, parfunc, funcdic)
    scan.run(batchsize=args.s, batches=args.b, threads=args.t)
