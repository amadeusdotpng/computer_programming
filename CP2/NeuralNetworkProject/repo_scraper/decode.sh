for f in *.txt; do
	base64 -D "$f" > "../decoded/$f"
done
