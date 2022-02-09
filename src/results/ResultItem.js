const ResultItem = ({ data }) => {
    const unit = data.unit !== "none" ? data.unit : "";
    const value = Number.isInteger(data.value) ? Math.round(data.value) : data.value.toFixed(2);

    return (
        <div className="resultitem">
            <div className="left">
                <h2>{data.description}</h2>
                <b>({data.why})</b>
            </div>
            <div className="right">
                <p>{value} {unit}</p>
                <p>Error: {(100 * data.relative_error).toFixed(2)}%</p>
                {/* <p><i>(score: {data.score})</i></p> */}
            </div>
        </div>
    )
}

export default ResultItem;