# __main__.py
import argparse
from cust_eval import fit, processing


def build_beta_geo_model(input_filepath):
	"""
	Fits a BG-NBD model from a .csv that contains the columns 'CustomerID', 'Timestamp' and 'PurchaseValue'.
	The Summary will
	:param input_filepath:
	:return: pd.dataframe with columns: ['CustomerID',
	'frequency',
	'recency',
	'T',
	'monetary_value',
	'predicted_purchases',
	'predicted_clv',
	'estimated_monetary_value']
	"""
	df = processing.read_df(input_filepath)
	if df is None:
		return None
	summary = processing.build_summary_from_df(df)
	results = fit.fit_beta_geo(summary)
	return results


def count(n, input_filepath, output): # predicted_purchases
	"""
	Writes a dataframe with the top N most frequent purchases

	:param n:(int) top n customers
	:param input_filepath:(str) .csv file path
	:param output:(str) write filepath
	:return: None
	"""
	results = build_beta_geo_model(input_filepath)
	if results is None:
		return
	results = results[["CustomerID", "num_predicted_purchases"]].reset_index()
	df_to_write = results.sort_values(by=['num_predicted_purchases'], ascending=False).head(n)
	processing.write_csv(output, df_to_write, "count.csv")


def spend(n, input_filepath, output_filepath): # predicted_clv
	"""
	Writes a dataframe with the top N highest spending customers.

	:param n: (int) top n customers
	:param input_filepath:(str) .csv file path
	:param output_filepath:(str) write filepath
	:return: None
	"""
	results = build_beta_geo_model(input_filepath)
	if results is None:
		return
	results = results[["CustomerID", "monetary_value", "predicted_clv"]].reset_index()
	df_to_write = results.sort_values(by=['monetary_value'], ascending=False).head(n)
	processing.write_csv(output_filepath, df_to_write, "spend.csv")


def main():
	global_parser = argparse.ArgumentParser(prog="cust-eval")
	subparsers = global_parser.add_subparsers(title="subcommands", help="count or spend")

	# Count Params
	count_parser = subparsers.add_parser("count",help="Sort customers by highest predicted number of purchases.")
	count_parser.add_argument("-n", required=True, help="Top number of customers to be returned. Required.")
	count_parser.add_argument("--input", required=True,
							  help="Input .csv file with columns 'CustomerID', 'Timestamp' and 'PurchaseValue'. Required.")
	count_parser.add_argument("--output", required=True, help="Location to write .csv file. Required.")
	count_parser.set_defaults(func=count)

	# Spend Params
	spend_parser = subparsers.add_parser("spend", help="Sort customers by highest predicted value of purchases.")
	spend_parser.add_argument("-n", required=True, help="Top number of customers to be returned. Required.")
	spend_parser.add_argument("--input", required=True,
							  help="Input .csv file with columns 'CustomerID', 'Timestamp' and 'PurchaseValue'. Required.")
	spend_parser.add_argument("--output", required=True, help="Location to write .csv file. Required.")
	spend_parser.set_defaults(func=spend)
	args = global_parser.parse_args()

	# Required Params
	n = int(args.n)
	input_filepath = args.input
	output_filepath = args.output
	run_function = args.func
	run_function(n, input_filepath, output_filepath)


if __name__ == "__main__":
	main()
