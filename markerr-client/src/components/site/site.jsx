import {h, render} from "preact";
import { useEffect } from "preact/hooks";
import { useStore } from "../../annotator/store";


const Site = (props) => {
    const {id} = props;
    const [site,] = useStore.site();

    useEffect(() => {console.log(id)}, []);

    return (
        <div>
            {id === "" && <div>Site doesn't exist</div>}
            {id !== "" && site && <div>{site.display_name}</div>}
        </div>
    );
}

export default Site;
