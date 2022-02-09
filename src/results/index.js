import useSearch from "../hooks/useSearch"
import "./results.css"

const ResultItem = ({ data }) => {
    console.log(data);
    return (
        <div className="resultitem">
            <p><b>({data.why})</b>: {data.description}</p>
            <p>{data.value.toFixed(2)} {data.unit} <i>(score: {data.score})</i></p>
        </div>
    )
}

const Results = ({ searchTerms }) => {
    const searchResults = useSearch(searchTerms);

    return (
        <div className="result transparentbox">
            {searchResults.map(e => <ResultItem data={e} />)}
        </div>
    )
}

export default Results;