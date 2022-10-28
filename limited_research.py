import pandas
import scipy.stats
import numpy


def summary_cont(group1, conf = 0.95, decimals = 4):



    conf_level = f"{round(conf * 100)}%"

    if type(group1) == pandas.core.series.Series:

        #### PUTTING THE INFORMATION INTO A DATAFRAME #####
        table = pandas.DataFrame(numpy.zeros(shape= (1,7)),
                         columns = ['Variable', 'N', 'Mean', 'SD', 'SE', f'{conf_level} Conf.', 'Interval'])


        # Setting up the first column (Variable names)
        table.iloc[0,0] = group1.name

        # Setting up the second column (Number of observations)
        table.iloc[0,1] = group1.count()

        # Setting up the third column (Mean)
        table.iloc[0,2] = numpy.mean(group1)

        # Setting up the fourth column (Standard Deviation (SD))
        table.iloc[0,3] = numpy.std(group1, ddof= 1)

        # Setting up the fith column (Standard Error (SE))
        table.iloc[0,4] = scipy.stats.sem(group1, nan_policy= 'omit')

        # Setting up the sixth and seventh column (95% CI)
        table.iloc[0,5], table.iloc[0,6] = scipy.stats.t.interval(conf,
                                          group1.count() - 1,
                                          loc= numpy.mean(group1), scale= scipy.stats.sem(group1, nan_policy= 'omit'))

    elif type(group1) == pandas.core.frame.DataFrame:

        table = pandas.DataFrame(numpy.zeros(shape= (1,7)),
                         columns = ['Variable', 'N', 'Mean', 'SD', 'SE',
                                    f'{conf_level} Conf.', 'Interval'])

        count = 0

        for ix, df_col in group1.iteritems():

            count = count + 1

            if count == 0:

                table = pandas.DataFrame(numpy.zeros(shape= (1,7)),
                         columns = ['Variable', 'N', 'Mean', 'SD', 'SE',
                                    f'{conf_level} Conf.', 'Interval'])

                # Setting up the first column (Variable names)
                table.iloc[0,0] = ix

                # Setting up the second column (Number of observations)
                table.iloc[0,1] = df_col.count()

                # Setting up the third column (Mean)
                table.iloc[0,2] = numpy.mean(df_col)

                # Setting up the fourth column (Standard Deviation (SD))
                table.iloc[0,3] = numpy.std(df_col, ddof= 1)

                # Setting up the fith column (Standard Error (SE))
                table.iloc[0,4] = scipy.stats.sem(df_col, nan_policy= 'omit')

                # Setting up the sixth and seventh column (95% CI)
                table.iloc[0,5], table.iloc[0,6] = scipy.stats.t.interval(conf,
                                          df_col.count() - 1,
                                          loc= numpy.mean(df_col),
                                          scale= scipy.stats.sem(df_col, nan_policy= 'omit'))
            else:

                table_a = pandas.DataFrame(numpy.zeros(shape= (1,7)),
                         columns = ['Variable', 'N', 'Mean', 'SD', 'SE',
                                    f'{conf_level} Conf.', 'Interval'])

                # Setting up the first column (Variable names)
                table_a.iloc[0,0] = ix

                # Setting up the second column (Number of observations)
                table_a.iloc[0,1] = df_col.count()

                # Setting up the third column (Mean)
                table_a.iloc[0,2] = numpy.mean(df_col)

                # Setting up the fourth column (Standard Deviation (SD))
                table_a.iloc[0,3] = numpy.std(df_col, ddof= 1)

                # Setting up the fith column (Standard Error (SE))
                table_a.iloc[0,4] = scipy.stats.sem(df_col, nan_policy= 'omit')

                # Setting up the sixth and seventh column (95% CI)
                table_a.iloc[0,5], table_a.iloc[0,6] = scipy.stats.t.interval(conf,
                                          df_col.count() - 1,
                                          loc= numpy.mean(df_col),
                                          scale= scipy.stats.sem(df_col, nan_policy= 'omit'))



            table = pandas.concat([table, table_a], ignore_index= "true")

        table.drop(0, inplace= True)
        table.reset_index(inplace= True, drop= True)



    elif type(group1) == pandas.core.groupby.SeriesGroupBy:
        ## Validated with R

        cnt = group1.count()
        cnt.rename("N", inplace= True)
        mean = group1.mean()
        mean.rename("Mean", inplace= True)
        std = group1.std(ddof= 1)
        std.rename("SD", inplace= True)
        se = group1.sem()
        se.rename("SE", inplace= True)

        # 95% CI
        l_ci, u_ci = scipy.stats.t.interval(conf,
                                          cnt - 1,
                                          loc= group1.mean(),
                                          scale= group1.sem())

        table = pandas.concat([cnt, mean, std, se,
                               pandas.Series(l_ci, index = cnt.index),
                               pandas.Series(u_ci, index = cnt.index)],
                              axis= 'columns')

        table.rename(columns = {'count': 'N', 'mean': 'Mean', 'std': 'SD',
                                'sem': 'SE', 0 : f'{conf_level} Conf.', 1 : "Interval" },
                                inplace= True)


    elif type(group1) == pandas.core.groupby.DataFrameGroupBy :

        # There has to be a better way to get the lower and upper CI limits
        # in the groupby table. Until then, this works :/
        def l_ci(x):
            l_ci, _ = scipy.stats.t.interval(conf,
                                                x.count() - 1,
                                                loc= x.mean(),
                                                scale= x.sem())


            return l_ci

        def u_ci(x):
            _, u_ci = scipy.stats.t.interval(conf,
                                                x.count() - 1,
                                                loc= x.mean(),
                                                scale= x.sem())


            return u_ci

        table = group1.agg(['count', numpy.mean, numpy.std,
                            pandas.DataFrame.sem, l_ci, u_ci])

        table.rename(columns = {'count': 'N', 'mean': 'Mean', 'std': 'SD',
                                'sem': 'SE', "l_ci" : f'{conf_level} Conf.', "u_ci" : "Interval"}, inplace= True)


    else:
        return "This method only works with a Pandas Series, Dataframe, or Groupby object"


    print("\n")
    return table.round(decimals)
